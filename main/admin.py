from django.contrib import admin
from .models import UserProfile,Team,Role,Game,RegOfTournaments,Tournament
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(Role)
admin.site.register(Game)
admin.site.register(RegOfTournaments)