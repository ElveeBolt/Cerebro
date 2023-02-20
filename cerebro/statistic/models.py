from django.db import models


# Create your models here.
class Statistics(models.Model):
    documents = models.IntegerField(null=True, verbose_name='Количество записей')
    indexes = models.IntegerField(null=True, verbose_name='Источников данных')
    size = models.FloatField(null=True, verbose_name='Размер данных')
    users = models.IntegerField(null=True, verbose_name='Пользователей')
    queries = models.IntegerField(null=True, verbose_name='Запросов')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"{self.documents}"

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'История статистики'
