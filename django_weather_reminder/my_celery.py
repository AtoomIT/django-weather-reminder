import os
from celery import Celery
from celery.schedules import crontab  # Додамо імпорт для crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_weather_reminder.settings')

app = Celery('django_weather_reminder')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.worker_pool = 'solo'

app.conf.beat_schedule = {
    'send_weather_updates_every_day_at_13_50': {
        'task': 'core.tasks.send_weather_updates',
        'schedule': crontab(hour='14', minute='22'),
    },
}

app.conf.timezone = 'Europe/Kiev'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
