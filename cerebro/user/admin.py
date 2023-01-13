from django.contrib import admin
from .models import Profile, Division, History, Login

# Register your models here.
admin.site.register(Division)

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'division')
    list_filter = ('user', 'division')

@admin.register(History)
class History(admin.ModelAdmin):
    list_display = ('user', 'query', 'date', 'total')
    list_filter = ('user', 'date')

@admin.register(Login)
class Login(admin.ModelAdmin):
    list_display = ('user', 'ip', 'date')
    list_filter = ('user', 'ip', 'date')
    readonly_fields = ['user', 'ip', 'user_agent', 'cookies', 'date']