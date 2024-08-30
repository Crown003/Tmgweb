from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
import os

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("", views.home, name="Home"),
    path("UserSignIn", views.UserSignIn, name="SignIn"),
    path("UserSignUp", views.UserSignUp, name="SignUp"),
    path("signout", views.signout, name="SignOut"),
    path("about", views.about, name="About"),
    path("contact", views.contact, name="Contact"),
    path("managmentSite", views.manageSite, name="Management"),
    path("gamingArea", views.gamingArea, name="GamingArea"),
    path("gameDetails", views.userGameDetails, name="UserGameDetails"),
    path("userProfile", views.userProfile, name="UserProfile"),
    path("editUserProfile", views.editUserProfile, name="EditUserProfile"),
    path("editTeamDetails/<int:id>", views.editTeamDetails, name="EditTeamDetails"),
    path("delTeam/<int:id>", views.deleteTeam, name="DeleteTeam"),
    path("viewTeamDetails/<int:id>", views.viewTeamDetails, name="viewTeamDetails"),
    path("tournamentPage", views.TournamentPage, name="Tournament"),
    path(
        "tournamentDetails/<int:id>",
        views.viewTournamentPage,
        name="UserViewTournament",
    ),
    path("deleteUserProfile", views.deleteUserProfileImage, name="DeleteProfileImage"),
    path(
        "orgainsertournamentDetails/<int:id>",
        views.viewTournament,
        name="OrgViewTournament",
    ),
    path("createGroups", views.createGroup, name="CreateGroups"),
    path("viewGroupsAdmin/<int:id>", views.viewGroups, name="ViewGroupsAdmin"),
    path("createRoadmap/<int:id>", views.createRoadmap, name="createRoadmap"),
    path("notification", views.notificationService, name="notification"),
    path("api/User", views.getUser, name="GetUser"),
    path("test/", views.test, name="test"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
