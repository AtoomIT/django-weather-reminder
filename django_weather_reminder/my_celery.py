import os
from celery import Celery
from celery.schedules import crontab  # Додамо імпорт для crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_weather_reminder.settings')

app = Celery('django_weather_reminder')

# Загрузка налаштувань з файлу settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Додамо наступний рядок
app.conf.worker_pool = 'solo'


# Налаштування для регулярного запуску задач
app.conf.beat_schedule = {
    'send_weather_updates_every_day_at_8_20': {
        'task': 'core.tasks.send_weather_updates',
        'schedule': crontab(hour='8', minute='20'),
    },
}

app.conf.timezone = 'Europe/Kiev'  # Місцевий час для України

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
