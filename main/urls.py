from django.urls import path
from . import views
from django.conf.urls.static import static
import os
urlpatterns = [
    path("",views.home,name="Home"),
    path("UserSignIn",views.UserSignIn,name="SignIn"),
    path("UserSignUp",views.UserSignUp,name="SignUp"),
    path("signout",views.signout,name="SignOut"),
    path("about",views.about,name="About"),
    path("contact",views.home,name="Contact"),
    path("managmentSite",views.manageSite,name="Management"),
    path("gamingArea",views.gamingArea,name="GamingArea"),
    path("gameDetails",views.userGameDetails,name="UserGameDetails"),
    path("userProfile",views.userProfile,name="UserProfile"),
    path("editUserProfile",views.editUserProfile,name="EditUserProfile"),
    path("editTeamDetails/<int:id>",views.editTeamDetails,name="EditTeamDetails"),
    path("delTeam/<int:id>",views.deleteTeam,name="DeleteTeam"),
    path("tournamentPage",views.TournamentPage,name="Tournament"),
    path("tournamentDetails/<int:id>",views.viewTournamentPage,name="UserViewTournament"),
    path("orgainsertournamentDetails/<int:id>",views.viewTournament,name="OrgViewTournament"),
	path("api/User",views.getUser,name="GetUser")
] + static("/media/",document_root = os.path.join(os.path.abspath(__file__),"/media/"))