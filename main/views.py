#pylint:disable=E1101
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import (UserRegistration,UserLogin,MatchData,
CreateTeamForm,EditProfileForm,EditTeamForm,EditUserForm,UserRegRoleForm)
from .models import UserProfile,Team,Tournament,RegOfTournaments,Game
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def manageSite(request):
	if request.user.userprofile.is_organiser != True:
		messages.warning(request,"You are not a organiser.")
		return redirect("UserProfile")
	orgTourny = Tournament.objects.filter(manager=request.user)
	return render(request,"managementSite.html",{"tournaments":orgTourny})

def UserSignIn(request):
	form = UserLogin()
	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"].strip().lower()
			password = form.cleaned_data["password"]
			user = authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
				messages.success(request,"Logged In successfully.")
				return redirect("Home")
	return render(request,"SignIn.html",{"signinform":form})
	
def UserSignUp(request):
	form = UserRegistration()
	if request.method == "POST":
		data = UserRegistration(request.POST)
		if data.is_valid():
			username = data.cleaned_data["username"].strip().lower()
			email = data.cleaned_data["email"].lower()
			password = data.cleaned_data["password"]
			user = User.objects.create_user(username=username,email=email)
			user.set_password(password)
			user.save()
			user_profile = UserProfile.objects.create(user=user)
			user_profile.save()
			messages.success(request,"Your account created successfully.")	
		form = UserRegistration()
		return redirect("SignIn")
	return render(request,"SignUp.html",{"signupform":form})


def signout(request):
	logout(request)	
	messages.success(request,"Loggedout Successfully.")
	return redirect("Home")
	
	
def home(request):
	return render(request,"base.html")
	
def about(request):
	return render(request,"about.html")
	
def contact(request):
	return render(request,"contact.html")
	
	
def  gamingArea(request):
	return render(request,"gamingArea.html")

def userProfile(request):
	createTeam = CreateTeamForm()
	TeamData = Team.objects.filter(creator=request.user)
	if request.method == "POST":
		data = CreateTeamForm(request.POST)	
		if data.is_valid():
			creator = request.user
			teamname = data.cleaned_data["teamname"]
			teamBio = data.cleaned_data["teamBio"]
			game= data.cleaned_data["game"]
			numberOfPlayers = data.cleaned_data["numberOfPlayers"]
			task = Team(creator=creator,teamname=teamname,teamBio=teamBio,game=game,numberOfPlayers=numberOfPlayers)
			task.save()
			messages.success(request,"Team created successfully.")		
		else:
			messages.warning(request,"error")
			return redirect("UserProfile")
	return render(request,"userProfile.html",{"form":createTeam, "teamData":TeamData})

def editUserProfile(request):
	if request.method == 'POST':
		user_form = EditUserForm(request.POST, instance=request.user)
		profile_form = EditProfileForm(request.POST,instance=request.user.userprofile)
		#password_form = PasswordChangeForm(request.user, request.POST)
		if user_form.is_valid():
			user_form.save()
		if profile_form.is_valid():
			profile_form.save()	
		#if password_form.is_valid():
#			user = password_form.save()
#			update_session_auth_hash(request, user)  # Keep the user logged in
#			messages.success(request, "Password successfully updated!")
		messages.success(request, "Profile updated successfully!")
		return redirect('EditUserProfile')
	else:
		user_form = EditUserForm(instance=request.user)
		profile_form = EditProfileForm(instance=request.user.userprofile)
		#password_form = PasswordChangeForm(request.user)
	return render(request,"EditUserProfile.html",{'user_form': user_form,'profile_form':profile_form})

def userGameDetails(request):
	return HttpResponse(request,"gameDetails")


def deleteTeam(request,id):
	user = request.user
	data = Team.objects.get(creator=user,id=id)
	try:
		data.delete()
		messages.success(request,"Team Deleted successfully.")
		return redirect("UserProfile")
	except Exception as e:
		messages.error(request,"Something wents wrong unable to delete your team at this moment try agin later.")
		return redirect("UserProfile")

def editTeamDetails(request,id):
    instance = Team.objects.get(creator=request.user,id=id)	
    form = EditTeamForm(instance=instance)
    if request.method == "POST":
    	form = EditTeamForm(request.POST,instance=instance)
    	if form.is_valid():
    		form.save()
    		messages.success(request,"Prodile Updated successfully.")
    	else:
    		messages.warning(request,"Check Your details properly & Try again.")
    return render(request,"EditTeamDetails.html",{"form":form})		

def viewTournamentPage(request,id):
	#this window is for user side tournament view.
	tournamentDetails = Tournament.objects.get(id=id)
	return render(request,"tournamentDetails.html",{"tournament":tournamentDetails})

def viewTournament(request,id):
	#this window is for organiser side tournament view.
	if request.user.userprofile.is_organiser == True:
		tournament = Tournament.objects.get(id=id)
		registered_teams = RegOfTournaments.objects.filter(tournament=tournament)
		slots_left = (tournament.slots - len(registered_teams))
		return render(request,"viewTournament.html",{"tourny":tournament,"slots_left":slots_left,"tournamentDetails":registered_teams})
	else:
		return redirect("Home")

def TournamentPage(request):
	try:
		games = Game.objects.all()
		tournaments = Tournament.objects.all()
	except Game.DoesNotExist:
		messages.warning(request,"Something wents wrong. Unable to get tournaments at this moment please try again later after some time. ")
	return render(request, "Tournaments.html", {"games":games if games else [],"tournaments":tournaments if tournaments else []})