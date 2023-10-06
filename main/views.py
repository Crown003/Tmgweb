#pylint:disable=E1101
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import (UserResistration,UserLogin,MatchData,
CreateTeamForm,EditProfileForm,EditTeamForm,EditUserForm,UserRegRoleForm)
from .models import UserProfile,Team
#from django.contrib import sessions
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def manageSite(request):
	form = MatchData()
	if request.method == "POST":
		form = MatchData(request.POST)
		if form.is_valid():
			game = form.cleaned_data["game"].strip().lower()
			group = form.cleaned_data["group"]
			roomDate = form.cleaned_data["roomDate"]
			roomStartTiming = form.cleaned_data["roomStartTiming"]
			roomId = form.cleaned_data["roomId"]
			roompassword = form.cleaned_data["roomPassword"]
			print(game,group,roomDate,roomStartTiming,roomId,roompassword)
	return render(request,"managementSite.html",{"form":form})

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
				return redirect("Home")
	return render(request,"SignIn.html",{"signinform":form})
	
def UserSignUp(request):
	form = UserResistration()
	user_role_form = UserRegRoleForm()
	if request.method == "POST":
		data = UserResistration(request.POST)
		role = UserRegRoleForm(request.POST)
		if data.is_valid():
			username = data.cleaned_data["username"].strip().lower()
			email = data.cleaned_data["email"].lower()
			password = data.cleaned_data["password"]
			user = User.objects.create_user(username=username,email=email)
			user.set_password(password)
			user.save()
			user_profile = UserProfile.objects.create(user=user)
			user_profile.save()	
			if role.is_valid():
				role.save()
			form = UserResistration()
			return redirect("SignIn")
	return render(request,"SignUp.html",{"signupform":form,"user_role_form":user_role_form})

def signout(request):
	request.session.flush()
	request.session["user"] = ""
	request.session["csrftoken"] = ""
	request.session["sessionid"] = ""
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
			try:
				task = Team(creator=creator,teamname=teamname,teamBio=teamBio,game=game,numberOfPlayers=numberOfPlayers)
				task.save()
				messages.success(request,"Team created successfully.")
			except Exception as e:
				messages.error(request,e)
				print(e)
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
		print(e)
		return redirect("UserProfile")

def editTeamDetails(request,id):
    instance = Team.objects.get(creator=request.user,id=id)	
    form = EditTeamForm(instance=instance)
    print(form.team_members)
    if request.method == "POST":
    	form = EditTeamForm(request.POST,instance=instance)
    	if form.is_valid():
    		messages.success(request,"DATA REACHED.")
    		print(request.POST)
    return render(request,"EditTeamDetails.html",{"form":form})		
