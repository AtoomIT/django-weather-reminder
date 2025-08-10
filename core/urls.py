from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('weather/', views.weather_list, name='weather_list'),
    path('subscriptions/', views.subscriptions_list_view, name='subscriptions_list'),
    path('subscriptions/add/', views.manage_subscription_view, name='add_subscription'),
    path('subscriptions/<int:subscription_id>/edit/', views.manage_subscription_view, name='edit_subscription'),
    path('subscriptions/<int:subscription_id>/delete/', views.delete_subscription_view, name='delete_subscription'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
]
