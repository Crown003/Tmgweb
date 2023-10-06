from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField()	
	def __str__(self):
		return f"{self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile_image = models.ImageField(upload_to="images/",default="static/images/Profile.png")
    roles = models.ManyToManyField('Role', related_name='user_profiles')
    selected_games = models.ManyToManyField(Game)  # Assuming you have a Game model
    bgmi_id = models.CharField(max_length=100,default="None")
    bgmi_ign = models.CharField(max_length=100,default="None")
    
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
	creator = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="team")
	created_on = models.DateTimeField(auto_now_add=True)
	teamname = models.CharField("Team Name",max_length=40,blank=False,unique=False)
	teamBio = models.TextField("Description",max_length=250,blank=False)
	game= models.OneToOneField(Game, on_delete=models.CASCADE,related_name="game")   
	numberOfPlayers = models.IntegerField(choices=MyIntegerChoices.choices)
	members = models.ManyToManyField(User, related_name='teams', blank=True)		
	def __str__(self):
		return f"{self.teamname}"

class Tournament(models.Model):
	name = models.CharField(max_length=100)
	main_image = models.ImageField(upload_to="images/",blank=True,null=True)
	logo = models.ImageField(upload_to="images/")
	slots = models.IntegerField("SLOTS",blank=True)
	starts_on = models.DateTimeField()
	ends_on = models.DateTimeField()
	def __str__(self):
		return str(self.name)

class RegOfTournaments(models.Model):
	regOn = models.DateTimeField(auto_now_add=True)
	regBy = models.OneToOneField(User,related_name='registeredBy', blank=True,on_delete=models.CASCADE)
	tournament = models.OneToOneField(Tournament, related_name='teams', blank=True,on_delete=models.CASCADE)
	team = models.OneToOneField(Team, related_name='teams', blank=True,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.tournament)+str(self.team)