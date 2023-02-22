from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Division, History, Login

# Register your models here.
admin.site.register(Division)

@admin.register(User)
class User(UserAdmin):
    model = User
    list_display = ['username', 'name', 'division', 'is_staff', 'is_active']
    list_filter = ['division', 'is_staff', 'is_active']

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Основные данные',
            {
                'fields': ['name', 'division', 'comment']
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Основные данные',
            {
                'fields': ['name', 'division', 'comment']
            }
        )
    )

@admin.register(History)
class History(admin.ModelAdmin):
    list_display = ('user', 'query', 'date', 'total')
    list_filter = ('user', 'date')

@admin.register(Login)
class Login(admin.ModelAdmin):
    list_display = ('user', 'ip', 'date')
    list_filter = ('user', 'ip', 'date')
    readonly_fields = ['user', 'ip', 'user_agent', 'cookies', 'date']