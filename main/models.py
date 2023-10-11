from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField()	
	def __str__(self):
		return f"{self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_organiser = models.BooleanField(default=False)
    user_profile_image = models.ImageField(upload_to="images/",default="static/images/Profile.png")
    roles = models.ManyToManyField('Role', related_name='user_profiles')
    selected_games = models.ManyToManyField(Game)  # Assuming you have a Game model
    BatttleGroundMobileIndia_id = models.CharField(max_length=100,default="None")
    BatttleGroundMobileIndia_ign = models.CharField(max_length=100,default="None")
    Volrant_id = models.CharField(max_length=100,default="None")
    Volrant_ign = models.CharField(max_length=100,default="None")
    ClashofClans_id = models.CharField(max_length=100,default="None")
    ClashofClans_ign = models.CharField(max_length=100,default="None")
    CallOfDuty_id = models.CharField(max_length=100,default="None")
    CallOfDuty_ign = models.CharField(max_length=100,default="None")
    def __str__(self):
        return f"{self.user.username}"

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
    	return str(self.name)
    	

class MyIntegerChoices(models.IntegerChoices):
    OPTION1 = 4, '4 players'
    OPTION2 = 5, '5 players'
    OPTION3 = 6, '6 players'
		
class Team(models.Model):
	creator = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="teamCreator")
	created_on = models.DateTimeField(auto_now_add=True)
	teamname = models.CharField("Team Name",max_length=40,blank=False,unique=True)
	teamBio = models.TextField("Description",max_length=250,blank=False)
	game= models.ForeignKey(Game, blank=True,null=True,on_delete=models.CASCADE,related_name="game")   
	numberOfPlayers = models.IntegerField(choices=MyIntegerChoices.choices)
	members = models.ManyToManyField(User, related_name='teamMembers', blank=True)		
	def __str__(self):
		return f"{self.teamname}"

class Tournament(models.Model):
	organiser = models.CharField(max_length=100,default="Tmg esports.")
	manager = models.ManyToManyField(User,related_name="tournamentManagers")
	name = models.CharField(max_length=100)
	description = models.TextField(null=True)
	game = models.ForeignKey(Game,related_name="tournamentGame", blank=True,on_delete=models.CASCADE,default="")
	main_image = models.ImageField(upload_to="images/",blank=True,null=True)
	logo = models.ImageField(upload_to="images/",blank=True,null=True)
	slots = models.IntegerField("SLOTS",blank=True)
	pricePool = models.IntegerField(default=0)
	is_paid = models.BooleanField(default=False)
	priceOfSlot = models.IntegerField(default=0)
	registrations_starts_from = models.DateTimeField(null=True,auto_now_add=True)
	registrations_ends_on = models.DateTimeField(null=True)
	starts_on = models.DateTimeField()
	ends_on = models.DateTimeField()
	def __str__(self):
		return str(self.name)

class RegOfTournaments(models.Model):
	regOn = models.DateTimeField(auto_now_add=True)
	regBy = models.OneToOneField(User,related_name='registeredBy', blank=True,on_delete=models.CASCADE)
	tournament = models.OneToOneField(Tournament, related_name='tournament', blank=True,on_delete=models.CASCADE)
	team = models.OneToOneField(Team, related_name='teamName', blank=True,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.tournament)+str(self.team)