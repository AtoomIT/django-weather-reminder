from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Subscription


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')  # Оновлено на username


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ('email', 'password')


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['city', 'country']
