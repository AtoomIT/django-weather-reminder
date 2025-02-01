from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Subscription


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'last_login')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('last_login',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональна інформація', {'fields': ('username',)}),
        ('Дозволи', {'fields': ()}),
        ('Дати', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'notification_period', 'created_at')
    search_fields = ('city', 'country', 'user__email')
    list_filter = ('created_at', 'notification_period')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
