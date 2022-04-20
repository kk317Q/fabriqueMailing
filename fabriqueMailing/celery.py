import os  
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriqueMailing.settings')
celery_app = Celery('fabriqueMailing')  
celery_app.config_from_object('django.conf:settings', namespace='CELERY')  
celery_app.autodiscover_tasks()  
