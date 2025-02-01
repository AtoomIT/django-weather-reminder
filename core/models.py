from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email є обов'язковим")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)  # Додаємо is_superuser
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):  # Наслідуємо PermissionsMixin
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)  # Необхідне поле
    is_active = models.BooleanField(default=True)  # Необхідне поле
    is_superuser = models.BooleanField(default=False)  # Додаємо is_superuser

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "Users"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notification_period = models.IntegerField(default=24)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_weathersubscription'
