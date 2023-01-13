from django.contrib import admin
from .models import Statistics

# Register your models here.
@admin.register(Statistics)
class Statistics(admin.ModelAdmin):
    list_display = ('documents', 'indexes', 'size', 'date')
    list_filter = ('documents', 'indexes', 'size', 'date')