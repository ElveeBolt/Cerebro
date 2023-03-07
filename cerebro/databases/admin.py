from django.contrib import admin
from .models import Database, Post, PostImage


# Register your models here.
class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Database)
class Database(admin.ModelAdmin):
    list_display = ('title', 'index', 'actuality', 'category', 'country')
    list_filter = ('actuality', 'category', 'country')
    inlines = (PostInline,)


class PostImageInline(admin.StackedInline):
    model = PostImage
    extra = 0
    readonly_fields = ('image_preview',)


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title', 'database')
    inlines = (PostImageInline,)


@admin.register(PostImage)
class PostImage(admin.ModelAdmin):
    list_display = ('image_preview', 'post')
    readonly_fields = ('image_preview',)
