from django.db import models

# Create your models here.
class HelpCategory(models.Model):
    title = models.CharField(null=False, max_length=255, verbose_name='Название категории')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Help(models.Model):
    title = models.CharField(null=False, max_length=255, verbose_name='Название вопроса')
    text = models.TextField(null=True, blank=True, verbose_name='Ответ')
    category = models.ForeignKey(HelpCategory, null=True, on_delete=models.SET_NULL, verbose_name='Категория')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы и ответы'