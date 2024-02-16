#pylint:disable=E1101
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import (UserRegistration,UserLogin,MatchData,
CreateTeamForm,EditProfileForm,CreateTournament,EditTeamForm,EditUserForm,TeamMemberForm)
from .models import UserProfile,Team,Tournament,RegOfTournaments,Game,TeamMember
from django.db import IntegrityError
from django.db.models import Q

# Create your views here.
def manageSite(request):
	if request.user.userprofile.is_organiser != True and request.user.userprofile.is_organiser_staff != True:
		messages.warning(request,"You are not a organiser/orgainsing staff.")
		return redirect("UserProfile")
	if request.method == "POST":
		createTournament = CreateTournament(request.POST)
		if createTournament.is_valid():
			managers = createTournament.cleaned_data["manager"]
			for user in managers:
				user_profile_to_update = UserProfile.objects.get(user__username=user)
				user_profile_to_update.is_organiser_staff = True
				user_profile_to_update.save()
			createTournament.save()
			messages.success(request,"Tournament created successfully.")
			return redirect("Management")
	createTournament = CreateTournament()
	orgTourny =Tournament.objects.filter(manager=request.user)
	print(orgTourny)
	return render(request,"managementSite.html",{"tournaments":orgTourny,"createTournamentForm":createTournament})

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
	return render(request,"home.html")
	
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
		if user_form.is_valid():
			user_form.save()
		if profile_form.is_valid():
			profile_form.save()	
		messages.success(request, "Profile updated successfully!")
		return redirect('EditUserProfile')
	else:
		user_form = EditUserForm(instance=request.user)
		profile_form = EditProfileForm(instance=request.user.userprofile)
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
	team_member_form = TeamMemberForm(instance=instance.members)
	if request.method == "POST":
		form = EditTeamForm(request.POST, instance=instance)
		team_member_form = TeamMemberForm(request.POST)
		if form.is_valid():
			team_member_instance = None
			if instance.members:
				team_member_instance = instance.members
				team_member_form = TeamMemberForm(request.POST, instance=team_member_instance)
			if team_member_form.is_valid():
				player_one = team_member_form.cleaned_data["player_one"]
				player_two = team_member_form.cleaned_data["player_two"]
				player_three = team_member_form.cleaned_data["player_three"]
				player_four = team_member_form.cleaned_data["player_four"]
				player_five = team_member_form.cleaned_data["player_five"]
				player_six = team_member_form.cleaned_data["player_six"]
				if not team_member_instance:
					data_of_players = TeamMember(
						player_one=player_one,
						player_two=player_two,
	                    player_three=player_three,
	                    player_four=player_four,
	                    player_five=player_five,
	                    player_six=player_six
	                )
					data_of_players.save()
					instance.members = data_of_players
				else:
					team_member_instance.player_one = player_one
					team_member_instance.player_two = player_two
					team_member_instance.player_three = player_three
					team_member_instance.player_four = player_four
					team_member_instance.player_five = player_five
					team_member_instance.player_six = player_six 
					team_member_form.save()    
				
				form.save()  # Save team details
				messages.success(request, "Team details updated successfully.")
				return redirect("UserProfile")
			else:
				print("Errors : ",team_member_form.errors)
				messages.warning(request,"Invalid Data ! Check Your details properly & Try again.")
	return render(request,"EditTeamDetails.html",{"form":form,"team_member_form":team_member_form})		

def viewTournamentPage(request,id):
	#this window is for user side tournament Details. view.
	tournamentDetails = Tournament.objects.get(id=id)
	if request.method == "POST":
		selectedTeamId = request.POST.get("teamId")
		regTeamDetails = Team.objects.get(id=int(selectedTeamId))
		print(regTeamDetails.members)
		if not regTeamDetails.members:
			messages.warning(request,"Your Team does'nt have 4 players, Complete your team and try again.")
			return render(request,"tournamentDetails.html",{"tournament":tournamentDetails})
		try:
			RegOfTournaments.objects.create(regBy=request.user,tournament=tournamentDetails,team=regTeamDetails)
			messages.success(request,"Registration successfull.")
			return redirect("UserProfile")
		except IntegrityError:
			messages.warning(request,"Team already registered.")
		except Exception:
			messages.error(request,"Oops something wents wrong please try again after some time.")
	return render(request,"tournamentDetails.html",{"tournament":tournamentDetails})

def viewTournament(request,id):
	#this window is for organiser side tournament Details view.
	if request.user.userprofile.is_organiser != True and request.user.userprofile.is_organiser_staff != True :
		messages.warning(request,"You are not a Organiser/Organiser staff")
		return redirect("Home")
	tournament = Tournament.objects.get(id=id)
	registered_teams = RegOfTournaments.objects.filter(tournament=tournament)
	slots_left = (tournament.slots - len(registered_teams))
	return render(request,"viewTournament.html",{"tourny":tournament,"slots_left":slots_left,"tournamentDetails":registered_teams})
		

def TournamentPage(request):
	# this view shows the Tournaments on portal.
	try:
		games = Game.objects.all()
		tournaments = Tournament.objects.all()
	except Game.DoesNotExist:
		messages.warning(request,"Something wents wrong. Unable to get tournaments at this moment please try again later after some time. ")
	return render(request, "Tournaments.html", {"games":games if games else [],"tournaments":tournaments if tournaments else []})
	
	
####api#####
from django.http import JsonResponse
def getUser(request):
    search_query = request.GET.get('search', '')
    users = UserProfile.objects.filter(user__username__startswith=search_query)
    # Serialize the queryset to JSON
    #print(users)
    users_data = [{'name': user.user.username, 'email': user.user.email} for user in users]
    return JsonResponse({'users': users_data})