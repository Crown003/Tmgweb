#pylint:disable=E1101
#pylint:disable=E1126
from django import forms
from django.utils import timezone
from main.models import UserProfile,Team,Game,Role,Tournament,TeamMember
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm



class UserRegistration(forms.Form):
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
	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)   
		selected_games = self.instance.selected_games.all()        
		for game in selected_games:
			self.fields[f"{game}.replace(" ","")_id"] = forms.CharField(label=f"{game} ID", required=False)
			self.fields[f"{game}.replace(" ","")_ign"] = forms.CharField(label=f"{game} IGN", required=False)

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
		model = TeamMember
		fields = "__all__"#["player_one","player_two","player_three","player_four","player_five","player_six"]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)# Iterate through all fields and add a class
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'team-member-username'
		
class EditTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['teamname', 'teamBio', 'game','numberOfPlayers']	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['teamname'].label = 'Team Name'
		self.fields['game'].label = 'Selected Game'
		self.fields['game'].queryset = Game.objects.all()  # Provide a queryset of available games
		
class DateInput(forms.DateInput):
	input_type = 'date'
	def __init__(self, attrs=None, format='%Y-%m-%d'):
		super().__init__(attrs={'data-date-format': format})

class CreateTournament(forms.ModelForm):
	class Meta:
		model = Tournament
		fields = "__all__"
		exclude = ["registrations_starts_from"]	
		widgets = {
		"registrations_ends_on":DateInput(),
		"starts_on":DateInput(),
		"ends_on":DateInput(),	
		}