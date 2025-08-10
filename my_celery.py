import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_weather_reminder.settings')

app = Celery('django_weather_reminder')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.worker_pool = 'solo'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
