from django.contrib import admin
from .models import HelpCategory, Help

# Register your models here.
admin.site.register(HelpCategory)


@admin.register(Help)
class Help(admin.ModelAdmin):
    list_display = ('title', 'category')