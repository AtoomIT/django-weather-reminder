from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import requests
import logging
from .models import User, Subscription
from .forms import SubscriptionForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.http import Http404


# Логгер
logger = logging.getLogger(__name__)


# Реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Реєстрація успішна. Тепер ви можете увійти.")
            return redirect('login')
        else:
            messages.error(request, "Помилка при реєстрації. Будь ласка, перевірте дані.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# Логін користувача
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile', username=user.username)
            else:
                messages.error(request, "Невірне ім'я користувача або пароль.")
        else:
            messages.error(request, "Помилка при логіні. Будь ласка, перевірте дані.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# Профіль користувача
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {
        'user': user,
        'show_weather_button': True,
        'show_subscriptions_button': True
    })


# Вихід з облікового запису
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# Головна сторінка
def home_view(request):
    return render(request, 'home.html')


# Сторінка погоди
def weather_list(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        country = request.POST.get('country')

        weather_info = get_weather(city, country)

        return render(request, 'weather/weather_list.html', {'weather_info': weather_info})

    return render(request, 'weather/weather_list.html')


# Функція для отримання погоди через API OpenWeatherMap
def get_weather(city, country):
    api_key = '657e5e0fc24a0baccf92dbce9551e328'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Помилка при отриманні погоди для {city}, {country}: {response.status_code}")
        return None


# Функція для отримання прогнозу погоди на 5 днів
def weather_forecast(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        country = request.POST.get('country')

        forecast_info = get_weather_forecast(city, country)

        return render(request, 'weather/weather_forecast.html', {'forecast_info': forecast_info})

    return render(request, 'weather/weather_forecast.html')


# Функція для отримання прогнозу погоди на 5 днів
def get_weather_forecast(city, country):
    api_key = '657e5e0fc24a0baccf92dbce9551e328'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Помилка при отриманні прогнозу погоди для {city}, {country}: {response.status_code}")
        return None


# Управління підписками
# Управління підписками
def manage_subscription_view(request, subscription_id=None):
    if not request.user.is_authenticated:
        messages.error(request, 'Ви повинні увійти в систему, щоб додавати або редагувати підписки.')
        return redirect('login')

    if subscription_id:
        subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    else:
        subscription = None

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            action = "оновлено" if subscription_id else "додано"
            logger.debug(f"Підписка для {request.user.email} {action}. Місто: {subscription.city}, Країна: {subscription.country}")
            messages.success(request, f'Підписка успішно {action}!')
            return redirect('subscriptions_list')
        else:
            logger.error(f"Помилка при збереженні підписки: {form.errors}")
            messages.error(request, "Помилка при додаванні/редагуванні підписки.")
    else:
        form = SubscriptionForm(instance=subscription)

    return render(request, 'subscriptions/manage_subscription.html', {'form': form, 'subscription': subscription})


def delete_subscription_view(request, subscription_id):
    try:
        subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    except Http404:
        raise Http404("Жодна підписка не відповідає даному запиту.")

    if request.method == "POST":
        subscription.delete()
        return redirect('subscriptions_list')  # Перенаправлення до списку підписок
    return redirect('subscriptions_list')  # Перенаправлення у випадку GET-запиту


# Відображення списку підписок
def subscriptions_list_view(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscriptions_list.html', {'subscriptions': subscriptions})


# Умови використання
def terms_of_service_view(request):
    return render(request, 'terms_of_service.html')


# Політика конфіденційності
def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

