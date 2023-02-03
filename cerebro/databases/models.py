from django.db import models


# Create your models here.
class Database(models.Model):
    title = models.CharField(null=False, max_length=255, verbose_name='Название источника')
    index = models.CharField(null=False, max_length=255, verbose_name='Кодовое название')
    actuality = models.IntegerField(null=True, blank=True, verbose_name='Актуальность данных')
    about = models.TextField(null=True, blank=True, verbose_name='Описание')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Список источников данных'