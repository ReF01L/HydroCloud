from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydroCloud.settings')

app = Celery('HydroCloud', broker='amqp://')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
