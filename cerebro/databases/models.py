from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class Database(models.Model):
    PROFILE_CHOICES = [
        (0, 'Не определена'),
        (1, 'Социальные профили'),
        (2, 'Политики'),
        (3, 'Военнослужащие')
    ]

    COUNTRY_CHOICES = [
        (None, 'Не определена'),
        ('rus', 'Россия'),
        ('ukr', 'Украина'),
    ]

    title = models.CharField(null=False, max_length=255, verbose_name='Название источника')
    index = models.CharField(null=False, max_length=255, unique=True, verbose_name='Кодовое название')
    actuality = models.IntegerField(null=True, blank=True, verbose_name='Актуальность данных')
    about = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.IntegerField(choices=PROFILE_CHOICES, default=0, verbose_name='Категория')
    country = models.CharField(null=True, blank=True, choices=COUNTRY_CHOICES, max_length=3, verbose_name='Страна')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Список источников данных'


class Post(models.Model):
    database = models.ForeignKey(Database, null=True, related_name='posts', on_delete=models.SET_NULL,
                                 verbose_name='Индекс')
    title = models.CharField(null=False, max_length=255, verbose_name='Название поста')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    url = models.CharField(null=True, blank=True, max_length=255, verbose_name='Источник')
    date_publish = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Список постов источника'


class PostImage(models.Model):
    post = models.ForeignKey(Post, null=True, related_name='images', on_delete=models.SET_NULL, verbose_name='Пост')
    image = models.ImageField(upload_to='posts', null=True, verbose_name='Изображение')

    def image_preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" />')

    image_preview.allow_tags = True
    image_preview.short_description = 'Изображение'

    def __str__(self):
        return f"{self.post}"

    class Meta:
        verbose_name = 'Фотографии'
        verbose_name_plural = 'Список фотографий поста'
