from django import forms
from django.utils import timezone
from main.models import UserProfile, Team, Game, Role, Tournament, TeamDetail
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserRegistration(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegRoleForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["user", "roles"]


class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class EditUserForm(UserChangeForm):
    model = User
    fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove unwanted fields from the form
        unwanted_fields = [
            "last_login",
            "date_joined",
            "is_superuser",
            "is_staff",
            "is_active",
            "password",
            "groups",
            "user_permissions",
            "first_name",
            "last_name",
            "staff_status",
        ]  # Add any other fields you want to exclude
        for field_name in unwanted_fields:
            if field_name in self.fields:
                del self.fields[field_name]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user", "is_organiser", "is_organiser_staff"]  # "user_profile_image"

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        selected_games = self.instance.selected_games.all()
        self.fields["selected_games"] = forms.ModelMultipleChoiceField(
            queryset=Game.objects.all(),
            required=False,
            label="Selected Games",
            widget=forms.CheckboxSelectMultiple,
        )


class MatchData(forms.Form):
    # game = forms.CharField(widget=forms.Select(choices=GAME_CHOICES))
    group = forms.CharField(
        widget=forms.Select(
            choices=[
                ("GROUP A", "A"),
                ("GROUP B", "B"),
                ("GROUP C", "C"),
                ("GROUP D", "D"),
            ]
        )
    )
    roomDate = forms.CharField(widget=forms.SelectDateWidget(), initial=timezone.now())
    roomStartTiming = forms.CharField(
        widget=forms.TimeInput(
            attrs={"placeholder": "enter time in this format - HH:MM (ex-9:00)"}
        )
    )
    roomId = forms.IntegerField()
    roomPassword = forms.CharField()


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["teamname", "teamBio", "game", "numberOfPlayers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teamname"].label = "Team Name"
        self.fields["game"].label = "Select Game"
        self.fields["game"].queryset = (
            Game.objects.all()
        )  # Provide a queryset of available games


class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["teamname", "teamBio", "game", "numberOfPlayers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teamname"].label = "Team Name"
        self.fields["game"].label = "Selected Game"
        self.fields["game"].queryset = (
            Game.objects.all()
        )  # Provide a queryset of available games


class EditTeamDetailsForm(forms.ModelForm):
    class Meta:
        model = TeamDetail
        exclude = ["details_of_team"]  # team_name exvluded form form.


class EditTeamDetailsForm(forms.ModelForm):
    class Meta:
        model = TeamDetail
        exclude = ["details_of_team"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["player_one"].required = False
        self.fields["player_two"].required = False
        self.fields["player_three"].required = False
        self.fields["player_four"].required = False
        self.fields["player_five"].required = False
        self.fields["player_one"].widget.attrs = {
            "placeholder": "Enter Player 1 Name (Igl)",
            "class": "player-name",
        }
        self.fields["player_two"].widget.attrs = {
            "placeholder": "Enter Player 2 Name ",
            "class": "player-name",
        }
        self.fields["player_three"].widget.attrs = {
            "placeholder": "Enter Player 3 Name ",
            "class": "player-name",
        }
        self.fields["player_four"].widget.attrs = {
            "placeholder": "Enter Player 4 Name ",
            "class": "player-name",
        }
        self.fields["player_five"].widget.attrs = {
            "placeholder": "Enter Player 5 Name ",
            "class": "player-name",
        }


class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, attrs=None, format="%Y-%m-%d"):
        super().__init__(attrs={"data-date-format": format})


class CreateTournament(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"
        exclude = ["registrations_starts_from", "created_by"]
        widgets = {
            "registrations_ends_on": DateInput(),
            "starts_on": DateInput(),
            "ends_on": DateInput(),
            "manager": forms.SelectMultiple(),
        }
