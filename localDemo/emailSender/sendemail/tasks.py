from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import counter
@shared_task
def send_mail_task():
    print("Mail sending.......")
    subject = 'm1 and m2 demo'
    message = f'Now I am testing m1 and m2 demo. there are {counter.objects.get(name="m1").amount} m1 and {counter.objects.get(name="m2").amount} m2' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['incredible749@163.com', ]
    send_mail( subject, message, email_from, recipient_list )
    return "Mail has been sent........"