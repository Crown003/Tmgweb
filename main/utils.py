from django.core.mail import send_mail
from django.conf import settings

def send_mail_to_user(user_email):
	subject = "TEST EMAIL FROM TMG PROJECT"
	message = "hello user ! welcome to the CROWN'S WORLD"
	from_email = settings.EMAIL_HOST_USER
	to_user = [user_email]
	send_mail(subject, message, from_email, to_user)