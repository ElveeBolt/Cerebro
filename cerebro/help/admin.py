from django.contrib import admin
from .models import HelpCategory, Help


# Register your models here.
class HelpInline(admin.StackedInline):
    model = Help
    extra = 0


@admin.register(HelpCategory)
class HelpCategory(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (HelpInline,)


@admin.register(Help)
class Help(admin.ModelAdmin):
    list_display = ('title', 'category')
