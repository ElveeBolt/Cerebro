from django.contrib import admin
from .models import Database, Post, PostImage


# Register your models here.
@admin.register(Database)
class Database(admin.ModelAdmin):
    list_display = ('title', 'index', 'actuality', 'category', 'country')
    list_filter = ('actuality', 'category', 'country')


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title', 'database')


@admin.register(PostImage)
class PostImage(admin.ModelAdmin):
    list_display = ('image_preview', 'post')
    readonly_fields = ('image_preview',)
