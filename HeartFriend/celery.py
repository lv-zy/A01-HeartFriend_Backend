from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HeartFriend.settings_prod')
app = Celery('HeartFriend')
app.conf.enable_utc=False

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')
app.conf.update(timezone='Asia/Shanghai')
# Load task modules from all registered Django apps.
# Celery Beat tasks registration
app.conf.beat_schedule = {
    'Send_message_to_Client': {
    'task': 'Health.tasks.send_message_task',
    'schedule': 30.0, 
    }, 
    'Send_email_to_Client': { 
        'task': 'Health.tasks.send_email_task', 
        'schedule': 600.0, 
    }
}

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')