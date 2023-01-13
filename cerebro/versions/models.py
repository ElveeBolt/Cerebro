from django.db import models

# Create your models here.
class Version(models.Model):
    title = models.CharField(null=False, max_length=255, verbose_name='Название обновления')
    version = models.CharField(null=False, max_length=20, verbose_name='Версия')
    date_update = models.CharField(null=True, max_length=50, blank=True, verbose_name='Дата выхода')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    update = models.TextField(null=True, blank=True, verbose_name='Что нового')
    fix = models.TextField(null=True, blank=True, verbose_name='Исправлено')

    def __str__(self):
        return f"{self.title}, {self.date_update}"

    class Meta:
        verbose_name = 'Обновление'
        verbose_name_plural = 'Список обновлений'