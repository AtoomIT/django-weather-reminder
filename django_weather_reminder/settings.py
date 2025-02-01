import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from celery.schedules import crontab

# Завантаження змінних із .env файлу
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key і Debug
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Installed Apps
INSTALLED_APPS = [
    'core.apps.CoreConfig',  # Вказуємо на конфігурацію CoreConfig
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.sites',
    'django_celery_beat',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL конфігурація
ROOT_URLCONF = 'django_weather_reminder.urls'

# Шаблони
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Використовуємо Path замість os.path.join
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'django_weather_reminder.wsgi.application'

# База даних SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'my_database.db'),  # Назва вашої БД
    }
}

# Налаштування для часу та локалі
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статичні файли
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Використовуємо Path замість os.path.join
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медійні файли
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Налаштування для Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Django REST Framework налаштування
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Користувацька модель
AUTH_USER_MODEL = 'core.User'

# Налаштування JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Email Backend (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# Логи
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'yourapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Безпека
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Налаштування для Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')  # URL брокера
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')  # URL для результатів
CELERY_ACCEPT_CONTENT = ['json']  # Формат повідомлень
CELERY_TASK_SERIALIZER = 'json'  # Сериалізатор задач
CELERY_RESULT_SERIALIZER = 'json'  # Сериалізатор результатів
CELERY_TIMEZONE = 'Europe/Kiev'

# Опціональні налаштування
CELERY_TASK_TRACK_STARTED = True  # Логування старту задачі
CELERY_TASK_TIME_LIMIT = 30 * 60  # Максимальний час виконання задачі (в секундах)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
SITE_ID = 1


CELERY_BEAT_SCHEDULE = {
    'send_weather_updates_everyday_at_1815': {
        'task': 'core.tasks.send_weather_updates',
        'schedule': crontab(hour='18', minute='15'),
    },
}
