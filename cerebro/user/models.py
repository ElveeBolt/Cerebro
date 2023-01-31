from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Division(models.Model):
    title = models.CharField(null=False, max_length=255, verbose_name='Название')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(null=True, max_length=255, verbose_name='Имя')
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL, verbose_name='Подразделение')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class History(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата и время')
    query = models.TextField(null=True, verbose_name='Поисковый запрос')
    total = models.IntegerField(null=True, verbose_name='Результатов поиска')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Поисковый запрос'
        verbose_name_plural = 'Поисковые запросы'


class Login(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    ip = models.CharField(null=True, max_length=255, verbose_name='IP адрес')
    user_agent = models.TextField(null=True, verbose_name='User Agent')
    cookies = models.TextField(null=True, verbose_name='Cookies')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата и время')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'История посещений'


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()