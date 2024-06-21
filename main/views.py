#pylint:disable=E1101
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import (UserRegistration,UserLogin,MatchData,
CreateTeamForm,EditProfileForm,CreateTournament,EditTeamForm,EditUserForm,EditTeamDetailsForm,EditTeamDetailsForm)
from .models import (UserProfile,Team,Tournament,
RegOfTournaments,Game,UserSupport,TeamDetail)
from django.db import IntegrityError
from django.db.models import Q
from .utils import send_mail_to_user

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
			try:
				send_mail_to_user(email) #in testing phase.
			except Exception as e:
				print("user signup is not sending email due to this error: " + str(e))
			return redirect("SignIn")
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
	if request.method == "POST":
		username = request.POST['Username'].lower().strip()
		subject = request.POST['Subject'].lower().strip()
		msg = request.POST['Message'].lower().strip()
		userSupportReq = UserSupport(
			user_real_name = username,
			request_subject = subject,
			request_message = msg,
			request_created_by = request.user
		)
		try:
			userSupportReq.save()
			messages.success(request,"Thank you for contacting us. We will reach out to you shortly.")		
		except Exception as e:
			print(e)
			messages.error(request,"Oops, something went wrong. Please try again later.")
		finally:
			return redirect("Contact")
	return render(request,"contact.html")
	
	
def  gamingArea(request):
	return render(request,"gamingArea.html")

def userProfile(request):
	createTeam = CreateTeamForm()
	TeamData = Team.objects.filter(creator=request.user)
	if request.method == "POST":
		data = CreateTeamForm(request.POST)	
		if data.is_valid():
			teamname = data.cleaned_data["teamname"]
			task = CreateTeamForm(request.POST)
			task.save(commit=False)
			task.instance.creator = request.user
			task.save()
			teamDetailsInst = TeamDetail(details_of_team = Team.objects.get(teamname=teamname))
			teamDetailsInst.save()
			messages.success(request,"Team created successfully.")		
		else:
			messages.warning(request,data.errors)
		return redirect("UserProfile")
	return render(request,"userProfile.html",{"form":createTeam, "teamData":TeamData,})

def editUserProfile(request):
	user_profile = get_object_or_404(UserProfile, user=request.user)
	user_selected_games = user_profile.selected_games.all()
	user_form = EditUserForm(instance=request.user)
	profile_form = EditProfileForm(instance=request.user.userprofile)
	if request.method == 'POST':
		user_form = EditUserForm(request.POST, instance=request.user)
		profile_form = EditProfileForm(request.POST,instance=request.user.userprofile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, "Profile updated successfully!")
		else:
			messages.error(request, "Oops something went wrong, Profile not updated!")
		return redirect('EditUserProfile')
	return render(request,"EditUserProfile.html",{'user_form': user_form,'profile_form':profile_form,})

def userGameDetails(request):
	return HttpResponse(request,"gameDetails")


def deleteTeam(request,id):
	user = request.user
	data = Team.objects.get(creator=user,id=id)
	print(id)
	try:
		data.delete()
		messages.success(request,"Team Deleted successfully.")
		return redirect("UserProfile")
	except Exception as e:
		messages.error(request,"Something wents wrong unable to delete your team at this moment try agin later.")
		return redirect("UserProfile")

def editTeamDetails(request,id):
	instanceOfTeam = Team.objects.get(creator=request.user,id=id)
	teamForm = EditTeamForm(instance=instanceOfTeam)
	instanceOfTeamDetail = TeamDetail.objects.get(details_of_team=instanceOfTeam.id)
	teamDetailForm = EditTeamDetailsForm(auto_id=True,instance=instanceOfTeamDetail)
	if request.method == "POST":
		teamForm = EditTeamForm(request.POST,instance=instanceOfTeam)
		teamDetailForm = EditTeamDetailsForm(request.POST,instance=instanceOfTeamDetail)
		try:
			if teamForm.is_valid():
				teamForm.save()  # Save team details
				messages.success(request, "Team details updated successfully.")
			if teamDetailForm.is_valid():
				task = teamDetailForm.save(commit=False)
				task.details_of_team = instanceOfTeam
				task.save()
		except Exception as EditTeamDetailsFormErrors:
			print("EditTeamDetailsFormErrors : " + str(EditTeamDetailsFormErrors))
		finally:
			return redirect("UserProfile")	
	return render(request,"EditTeamDetails.html",{"form":teamForm,"teamDetailForm":teamDetailForm})		

def viewTeamDetails(request,id):
	try:
		TeamDetailsData = TeamDetail.objects.get(details_of_team=id)
	except Exception as e:
		TeamDetailsData = ""
		print(e)
	return render(request,"ViewTeamDetails.html",{"teamDetails":TeamDetailsData})

def viewTournamentPage(request,id):
	#this window is for user side tournament Details. view.
	tournamentDetails = Tournament.objects.get(id=id)
	if request.method == "POST":
		selectedTeamId = request.POST.get("teamId")
		regTeam = Team.objects.get(id=selectedTeamId)
		regTeamDetails = TeamDetail.objects.get(details_of_team=int(selectedTeamId))
		if regTeamDetails.player_one == "" and regTeamDetails.player_two == "" and regTeamDetails.player_three and regTeamDetails.player_four == "" :
			messages.warning(request,"Your Team does'nt have 4 players, Complete your team and try again.")
			return redirect("Tournament")
		if regTeam.game != tournamentDetails.game:
			messages.warning(request,"The team you are trying to register is of different game ! check you details and try again.")
			return redirect("Tournament")
		try:
			RegOfTournaments.objects.create(regBy=request.user,tournament=tournamentDetails,team=regTeamDetails.details_of_team)
			messages.success(request,"Registration successfull.")
		except IntegrityError:
			messages.warning(request,"A team is  already registered from your account.")			
		except Exception:
			messages.error(request,"Oops something wents wrong please try again after some time.")
		finally:
			return redirect("UserProfile")
			
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

from django.http import JsonResponse
def getUser(request):
    search_query = request.GET.get('search', '')
    users = UserProfile.objects.filter(user__username__startswith=search_query)
    # Serialize the queryset to JSON:
    users_data = [{'name': user.user.username, 'email': user.user.email} for user in users]
    return JsonResponse({'users': users_data})