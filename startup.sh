#!/bin/bash

python3 manage.py collectstatic --noinput
python3 manage.py migrate
gunicorn django_weather_reminder.wsgi:application --bind=0.0.0.0 --timeout 600
