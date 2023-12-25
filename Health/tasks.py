from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model() 

@shared_task
def send_mail_task():
    print("Mail sending.......")
    subject = 'dev-emailSender'
    message = User.objects.all()  
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['incredible749@163.com', ]
    send_mail( subject, message, email_from, recipient_list )
    return "Mail has been sent........"