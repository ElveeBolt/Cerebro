from django.contrib import admin
from .models import Database

# Register your models here.
@admin.register(Database)
class Database(admin.ModelAdmin):
    list_display = ('title', 'index', 'actuality')
    list_filter = ('actuality',)