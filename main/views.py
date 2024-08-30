from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from .forms import (
    UserRegistration,
    UserLogin,
    MatchData,
    CreateTeamForm,
    EditProfileForm,
    CreateTournament,
    EditTeamForm,
    EditUserForm,
    EditTeamDetailsForm,
    EditTeamDetailsForm,
)
from .models import (
    UserProfile,
    Team,
    Tournament,
    RegOfTournaments,
    Game,
    UserSupport,
    TeamDetail,
    RoadmapRoundsDetail,
)
from django.db import IntegrityError
from django.db.models import Q
from .utils import send_mail_to_user, get_number_of_groups, is_groups_distributed
import json


# Create your views here.
def manageSite(request):
    if (
        request.user.userprofile.is_organiser != True
        and request.user.userprofile.is_organiser_staff != True
    ):
        messages.warning(request, "You are not an organiser/orgainsing staff.")
        return redirect("UserProfile")
    if request.method == "POST":
        createTournament = CreateTournament(request.POST, request.FILES)
        print(request.POST)
        if createTournament.is_valid():
            managers = createTournament.cleaned_data["manager"]
            for user in managers:
                user_profile_to_update = UserProfile.objects.get(user__username=user)
                user_profile_to_update.is_organiser_staff = True
                user_profile_to_update.save()
            createTournament.save(commit=False)
            createTournament.instance.created_by = request.user
            createTournament.save()
            messages.success(
                request,
                "Tournament created successfully.important:generate or upload your tournament roadmap.",
            )
            return redirect("Management")

    createTournament = CreateTournament()
    orgTourny = Tournament.objects.filter(
        created_by=request.user
    ) | Tournament.objects.filter(manager=request.user)
    return render(
        request,
        "managementSite.html",
        {"tournaments": orgTourny.distinct(), "createTournamentForm": createTournament},
    )


def UserSignIn(request):
    print(request.user.is_authenticated)
    form = UserLogin()
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].strip().lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In successfully.")
                return redirect("Home")
    return render(request, "SignIn.html", {"signinform": form})


def UserSignUp(request):
    form = UserRegistration()
    if request.method == "POST":
        data = UserRegistration(request.POST)
        if data.is_valid():
            username = data.cleaned_data["username"].strip().lower()
            email = data.cleaned_data["email"].lower()
            password = data.cleaned_data["password"]
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
            messages.success(request, "Your account created successfully.")
            try:
                send_mail_to_user(email)  # in testing phase.
            except Exception as e:
                print("user signup is not sending email due to this error: " + str(e))
            return redirect("SignIn")
        form = UserRegistration()
        return redirect("SignIn")
    return render(request, "SignUp.html", {"signupform": form})


def signout(request):
    logout(request)
    messages.success(request, "Loggedout Successfully.")
    return redirect("Home")


def home(request):
    return render(request, "home.html", {"room_name": "broadcast"})


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        if (
            request.POST["Username"] == ""
            and request.POST["Message"] == ""
            and request.POST["Subject"] == ""
        ):
            messages.warning(request, "Please fill the form correctly! ")
            return redirect("Contact")
        username = request.POST["Username"].lower().strip()
        subject = request.POST["Subject"].lower().strip()
        msg = request.POST["Message"].lower().strip()
        userSupportReq = UserSupport(
            user_real_name=username,
            request_subject=subject,
            request_message=msg,
            request_created_by=request.user,
        )
        try:
            # userSupportReq.save()
            messages.success(
                request,
                "Thank you for contacting us. We will reach out to you shortly.",
            )
        except Exception as e:
            print(e)
            messages.error(
                request, "Oops, something went wrong. Please try again later."
            )
        finally:
            return redirect("Contact")
    return render(request, "contact.html")


def gamingArea(request):
    return render(request, "gamingArea.html")


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
            teamDetailsInst = TeamDetail(
                details_of_team=Team.objects.get(teamname=teamname)
            )
            teamDetailsInst.save()
            messages.success(request, "Team created successfully.")
        else:
            messages.warning(request, data.errors)
        return redirect("UserProfile")
    return render(
        request,
        "userProfile.html",
        {
            "form": createTeam,
            "teamData": TeamData,
        },
    )


def editUserProfile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_selected_games = user_profile.selected_games.all()
    user_form = EditUserForm(instance=request.user)
    profile_form = EditProfileForm(instance=request.user.userprofile)
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Oops something went wrong, Profile not updated!")
        return redirect("EditUserProfile")
    return render(
        request,
        "EditUserProfile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


def deleteUserProfileImage(request):
    try:
        user_obj = UserProfile.objects.get(user=request.user)
        if user_obj.user_profile_image:
            user_obj.user_profile_image.delete(
                save=True
            )  # Delete and save changes in datafiles tooo.
            user_obj.save()
            messages.success(request, "Profile Image deleted successfully.")
        else:
            messages.warning(request, "No profile image found to delete.")
    except FileNotFoundError:
        messages.warning(request, "Profile image not found.")
    except Exception as e:
        messages.warning(request, "An error occurred: {0}".format(e))
    return redirect("UserProfile")


from asgiref.sync import async_to_sync
from django.shortcuts import HttpResponse
from channels.layers import get_channel_layer


def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {"type": "send_notification", "message": json.dumps("Notification")},
    )
    return HttpResponse("Done")


def notificationService(request):
    return render(request, "notification.html", {"room_name": "broadcast"})


def userGameDetails(request):
    return HttpResponse(request, "gameDetails")


def deleteTeam(request, id):
    user = request.user
    data = Team.objects.get(creator=user, id=id)
    try:
        data.delete()
        messages.success(request, "Team Deleted successfully.")
        return redirect("UserProfile")
    except Exception as e:
        messages.error(
            request,
            "Something wents wrong unable to delete your team at this moment try agin later.",
        )
        return redirect("UserProfile")


def editTeamDetails(request, id):
    instanceOfTeam = Team.objects.get(creator=request.user, id=id)
    teamForm = EditTeamForm(instance=instanceOfTeam)
    instanceOfTeamDetail = TeamDetail.objects.get(details_of_team=instanceOfTeam.id)
    teamDetailForm = EditTeamDetailsForm(auto_id=True, instance=instanceOfTeamDetail)
    if request.method == "POST":
        teamForm = EditTeamForm(request.POST, instance=instanceOfTeam)
        teamDetailForm = EditTeamDetailsForm(
            request.POST, instance=instanceOfTeamDetail
        )
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
    return render(
        request,
        "EditTeamDetails.html",
        {"form": teamForm, "teamDetailForm": teamDetailForm},
    )


def viewTeamDetails(request, id):
    try:
        TeamDetailsData = TeamDetail.objects.get(details_of_team=id)
        registrationData = RegOfTournaments.objects.filter(
            team=TeamDetailsData.details_of_team
        )
    except Exception as e:
        TeamDetailsData = ""
        print(e)
    return render(request, "ViewTeamDetails.html", {"teamDetails": TeamDetailsData})


def viewTournamentPage(request, id):
    # this window is for user side tournament Details. view.
    tournamentDetails = Tournament.objects.get(id=id)
    try:
        roadmapOfTournament = RoadmapRoundsDetail.objects.get(
            tournament=tournamentDetails
        )
        roadmapData = {}
        for i in [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
        ]:
            round_data = getattr(roadmapOfTournament, f"round_{i}", None)
            if round_data:
                roadmapData.update({f"Round {i}": round_data})
            else:
                break
    except:
        roadmapOfTournament = False
    if request.method == "POST":
        try:
            selectedTeamId = request.POST.get("teamId")
            regTeam = Team.objects.get(id=selectedTeamId)
            regTeamDetails = TeamDetail.objects.get(details_of_team=int(selectedTeamId))
            # if regTeamDetails.player_one == "" or regTeamDetails.player_two == "" or regTeamDetails.player_three or regTeamDetails.player_four == "" :
            # 				messages.warning(request,"Your Team does'nt have 4 players, Complete your team and try again.")
            # 				return redirect("Tournament")
            if regTeam.game != tournamentDetails.game:
                messages.warning(
                    request,
                    "The team you are trying to register is of different game ! check you details and try again.",
                )
                return redirect("Tournament")
            try:
                RegOfTournaments.objects.create(
                    regBy=request.user,
                    tournament=tournamentDetails,
                    team=regTeamDetails.details_of_team,
                )
                messages.success(request, "Registration successfull.")
            except IntegrityError:
                messages.warning(
                    request, "A team is  already registered from your account."
                )
            except Exception:
                messages.error(
                    request,
                    "Oops something wents wrong please try again after some time.",
                )
            finally:
                return redirect("UserProfile")
        except Exception as e:
            print(e)
            messages.error(
                request, "Team not found! please select a team and try again."
            )
            return redirect("Tournament")
    return render(
        request,
        "tournamentDetails.html",
        {
            "tournament": tournamentDetails,
            "roadmap": roadmapOfTournament,
        },
    )


def viewTournament(request, id):
    # this window is for organiser side tournament Details view.
    if (
        request.user.userprofile.is_organiser != True
        and request.user.userprofile.is_organiser_staff != True
    ):
        messages.warning(request, "You are not a Organiser/Organiser staff")
        return redirect("Home")
    tournament = Tournament.objects.get(id=id)
    registered_teams = RegOfTournaments.objects.filter(tournament=tournament)
    slots_left = tournament.slots - len(registered_teams)
    return render(
        request,
        "viewTournament.html",
        {
            "tourny": tournament,
            "slots_left": slots_left,
            "tournamentDetails": registered_teams,
        },
    )


def createGroup(request):
    """
    a bit of improvement needed in the group distribution logic it is right now not good enough...
    to handle data.
    issue: the data adds each time we create groups into db! irrespective of the data was previously added or not.
    """
    if request.method == "POST":
        reg_team_object = RegOfTournaments.objects.filter(
            tournament=request.POST.get("tournament_id")
        )
        total_teams_count = reg_team_object.count()
        team_in_a_group = int(
            request.POST["teamInAGroup"]
        )  # number of teams in each group.
        a = get_number_of_groups(total_teams_count, team_in_a_group)
        group_data = {}
        group_number = 1
        if a["statusOfGroups"] == "All":
            for i in range(0, total_teams_count, team_in_a_group):
                teams_batch = reg_team_object[i : i + team_in_a_group]
                data_of_one_group = {
                    f"group{group_number}": [x.id for x in teams_batch]
                }
                group_data.update(data_of_one_group)
                group_number += 1
                data_of_one_group = {}
            group_number = 1
            task, created = RoadmapRoundsDetail.objects.get_or_create(
                tournament=Tournament.objects.model(
                    id=request.POST.get("tournament_id"), created_by=request.user
                )
            )
            print(group_data)
            match request.POST["round"]:
                case "one":
                    _data = task.round_one
                    _data.update({"groupData": group_data})
                    task.round_one = _data
                case "two":
                    _data = task.round_two
                    _data.update({"groupData": group_data})
                    task.round_two = _data
                case "three":
                    _data = task.round_three
                    _data.update({"groupData": group_data})
                    task.round_three = _data
                case "four":
                    _data = task.round_four
                    _data.update({"groupData": group_data})
                    task.round_four = _data
                case "five":
                    _data = task.round_five
                    _data.update({"groupData": group_data})
                    task.round_five = _data
                case "six":
                    _data = task.round_six
                    _data.update({"groupData": group_data})
                    task.round_six = _data
                case "seven":
                    _data = task.round_seven
                    _data.update({"groupData": group_data})
                    task.round_seven = _data
                case "eight":
                    _data = task.round_eight
                    _data.update({"groupData": group_data})
                    task.round_eight = _data
                case "nine":
                    _data = task.round_nine
                    _data.update({"groupData": group_data})
                    task.round_nine = _data
                case "ten":
                    _data = task.round_ten
                    _data.update({"groupData": group_data})
                    task.round_ten = _data
            try:
                task.save()
                messages.success(request, "Round details updated successfully!")
            except Exception as e:
                messages.error(request, str(e))
    return redirect("UserProfile")


def TournamentPage(request):
    # this view shows the Tournaments on portal.
    try:
        games = Game.objects.all()
        tournaments = Tournament.objects.all()
    except Game.DoesNotExist:
        messages.warning(
            request,
            "Something wents wrong. Unable to get tournaments at this moment please try again later after some time. ",
        )
    return render(
        request,
        "Tournaments.html",
        {
            "games": games if games else [],
            "tournaments": tournaments if tournaments else [],
        },
    )


def viewGroups(request, id):
    if request.method == "POST":
        try:
            data = RoadmapRoundsDetail.objects.get(tournament=id)
        except Exception as e:
            if "RoadmapRoundsDetail matching query does not exist" in str(e):
                messages.warning(request, "Teams Distribution is not happened yet.")
            return redirect(reverse("ViewGroupsAdmin", args=[id]))
        match request.POST["round"]:
            case "one":
                data = data.round_one
                print(data)
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data["groupData"].items()}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "two":
                data = data.round_two
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "three":
                data = data.round_three
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "four":
                data = data.round_four
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "five":
                data = data.round_five
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "six":
                data = data.round_six
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "seven":
                data = data.round_seven
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "eight":
                data = data.round_eight
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "nine":
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                data = data.round_nine
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
            case "ten":
                data = data.round_ten
                if not data:
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                if not is_groups_distributed(data):
                    messages.warning(request, "groups are not distributed yet.")
                    return redirect(reverse("ViewGroupsAdmin", args=[id]))
                filtered_data = {k: v for k, v in data.items() if "group" in k}
                teams_data = {}
                for item in filtered_data:
                    queryobject = RegOfTournaments.objects.filter(
                        id__in=filtered_data[item]
                    )
                    teams_data[item] = list(
                        queryobject.values_list("team__id", "team__teamname")
                    )
        request.session["teams_data"] = teams_data
        return redirect(reverse("ViewGroupsAdmin", args=[id]))
    teams_data = request.session.get("teams_data", {})
    request.session.pop("teams_data", None)
    return render(request, "groupsAdminView.html", {"groups_data": teams_data})


def createRoadmap(request, id):
    if request.method == "POST":
        rounds = []
        for i in range(1, 11):
            round_name = request.POST.get(f"round_name_{i}")
            teams_in_round = request.POST.get(f"number_of_teams_{i}")
            advancing_teams = request.POST.get(f"teams_qualify_{i}")
            is_last_round = request.POST.get(f"last_round_{i}")
            if is_last_round == "on":
                if (round_name and teams_in_round) or advancing_teams:
                    temp = {
                        "roundName": round_name,
                        "teamsInRound": teams_in_round,
                        "advancingTeams": advancing_teams,
                    }
                    rounds.append(temp)
                    break
            else:
                if round_name and teams_in_round and advancing_teams:
                    temp = {
                        "roundName": round_name,
                        "teamsInRound": teams_in_round,
                        "advancingTeams": advancing_teams,
                    }
                    rounds.append(temp)
                    continue
        try:
            help_str = [
                "round_one",
                "round_two",
                "round_three",
                "round_four",
                "round_five",
                "round_six",
                "round_seven",
                "round_eight",
                "round_nine",
                "round_ten",
            ]  # Using help_str to frame the field names of the model RoadmapRoundsDetails
            task = RoadmapRoundsDetail(
                tournament=Tournament.objects.get(id=id), created_by=request.user
            )
            task.save()
            task, createdOBJ = RoadmapRoundsDetail.objects.get_or_create(
                tournament=Tournament.objects.get(id=id), created_by=request.user
            )
            for index, round_data in enumerate(rounds):
                if round_data:  # Ensure that there is data to be set
                    setattr(task, help_str[index], round_data)
                else:
                    break
            task.save()
            messages.success(request, "Roadmap Created Successfully.")
        except Exception as e:
            print(e)
            messages.warning(
                request, "Something went wrong! Check your data and try again."
            )
        finally:
            return redirect(reverse("OrgViewTournament", args=[id]))
    return render(request, "roadmapForm.html", {"list": [x for x in range(1, 11)]})


from django.http import JsonResponse


def getUser(request):
    search_query = request.GET.get("search", "")
    users = UserProfile.objects.filter(user__username__startswith=search_query)
    # Serialize the queryset to JSON:
    users_data = [
        {"name": user.user.username, "email": user.user.email} for user in users
    ]
    return JsonResponse({"users": users_data})
