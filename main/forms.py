#pylint:disable=E1101
#pylint:disable=E1126
from django import forms
from django.utils import timezone
from main.models import UserProfile,Team,Game,Role
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms import formset_factory

ROLE_CHOICES= [
    ('teamManager', 'Team Manager'),
    ('player', 'Player'),
    ('none', 'Guest'),
    ]

class UserResistration(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())

class UserRegRoleForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ["user","roles"]	

class UserLogin(forms.Form):
	username = forms.CharField()
	password= forms.CharField(widget=forms.PasswordInput())

class EditUserForm(UserChangeForm):
	model = User
	fields = ["username","email"]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Remove unwanted fields from the form
		unwanted_fields = ['last_login','date_joined','is_superuser','is_staff','is_active','password','groups','user_permissions','first_name','last_name','staff_status']  # Add any other fields you want to exclude
		for field_name in unwanted_fields:
			if field_name in self.fields:
				del self.fields[field_name]
		
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'roles', 'selected_games']
    

class MatchData(forms.Form):
	#game = forms.CharField(widget=forms.Select(choices=GAME_CHOICES))
	group = forms.CharField(widget=forms.Select(choices=[("GROUP A","A"),("GROUP B","B"),("GROUP C","C"),("GROUP D","D")]))
	roomDate = forms.CharField(widget=forms.SelectDateWidget(),initial=timezone.now())
	roomStartTiming = forms.CharField(widget=forms.TimeInput(attrs={"placeholder" : "enter time in this format - HH:MM (ex-9:00)"}))
	roomId = forms.IntegerField()
	roomPassword = forms.CharField()

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['teamname', 'teamBio', 'game','numberOfPlayers']
        exclude = ['members']
        def __init__(self, *args, **kwargs):
        	super().__init__(*args, **kwargs)
        	self.fields["teamname"].label = 'Team Name'
	        self.fields["game"].label = 'Select Game'
	        self.fields["game"].queryset = Game.objects.all()  # Provide a queryset of available games

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username']  # Include other fields as needed
        def __init__(self, *args, **kwargs):
        	super().__init__(*args, **kwargs)
        	self.fields['email'].label = "EMAIL"
        	self.fields['username'].label = "PLAYER"


TeamMemberFormSet = formset_factory(TeamMemberForm, extra=5)
class EditTeamForm(forms.ModelForm):
	team_members = TeamMemberFormSet()
	class Meta:
		model = Team
		fields = ['teamname', 'teamBio', 'game','numberOfPlayers']
		#exclude = ['members']
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields[0].label = 'Team Name'
			self.fields[2].label = 'Select Game'
			self.fields[2].queryset = Game.objects.all()  # Provide a queryset of available games