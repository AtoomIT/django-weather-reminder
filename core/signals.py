# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subscription
from .utils import send_weather_email
from .views import get_weather

@receiver(post_save, sender=Subscription)
def send_email_on_subscription(sender, instance, created, **kwargs):
    if created:
        weather_data = get_weather(instance.city, instance.country)
        if weather_data:
            send_weather_email(instance.user.email, instance.city, weather_data)
