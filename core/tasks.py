from celery import shared_task
from .models import Subscription
from .utils import send_weather_email
from .views import get_weather


@shared_task
def send_weather_updates():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        weather_data = get_weather(subscription.city, subscription.country)
        if weather_data:
            send_weather_email(subscription.user.email, subscription.city, weather_data)
