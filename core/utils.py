from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_weather_email(email, city, weather_data):
    subject = f"Прогноз погоди для {city}"
    message = render_to_string('emails/weather_email.html', {
        'city': city,
        'temperature': weather_data['main']['temp'],
        'feels_like': weather_data['main']['feels_like'],
        'temp_min': weather_data['main']['temp_min'],
        'temp_max': weather_data['main']['temp_max'],
        'wind_speed': weather_data['wind']['speed'],
        'cloudiness': weather_data['clouds']['all']
    })
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=message)