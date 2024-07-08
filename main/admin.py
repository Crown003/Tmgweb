from django.contrib import admin
from .models import (UserProfile,
Team,Role,Game,RegOfTournaments,Tournament,UserSupport,TeamDetail,RoadmapOfTournament,RoadmapRoundsDetail)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tournament)
admin.site.register(Role)
admin.site.register(Game)
admin.site.register(RegOfTournaments)
admin.site.register(RoadmapOfTournament)
admin.site.register(RoadmapRoundsDetail)
#registring the Usersupport model this way so that i can see the
# default hidden fields such as request_created_on etc..
class UserSupportReqAdmin(admin.ModelAdmin):
    list_display = ('user_real_name','request_subject','request_message', 'request_created_on')  # Display in the list view
    readonly_fields = ('request_created_on',)    # Display in the detail view as read-only

admin.site.register(UserSupport, UserSupportReqAdmin)
admin.site.register(Team)
admin.site.register(TeamDetail)

