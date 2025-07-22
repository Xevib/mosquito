import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.main.settings')

app = Celery('mosquito_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()