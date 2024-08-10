from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


def send_mail_to_user(user_email):
    """for sending emails to users"""
    subject = "TEST EMAIL FROM TMG PROJECT"
    message = "hello user ! welcome to the CROWN'S WORLD"
    from_email = settings.EMAIL_HOST_USER
    to_user = [user_email]
    send_mail(subject, message, from_email, to_user)


def get_number_of_groups(totalTeams, teamInAGrp):
    if totalTeams % teamInAGrp == 0:
        numberOfGroups = totalTeams // teamInAGrp
        return {"statusOfGroups": "All", "TotalGroups": numberOfGroups}
    else:
        numberOfGroups = totalTeams // teamInAGrp
        remainingTeam = totalTeams % teamInAGrp
        return {
            "statusOfGroups": "All",
            "TotalGroups": numberOfGroups,
            "RemainingTeams": remainingTeam,
        }


def is_groups_distributed(data):
    for key in data.keys():
        if "group" in key:
            return True
    return False
