from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save


class User(AbstractUser):

    bio = models.TextField('Описание профиля', blank=True, null=True)
    email = models.EmailField('Почта пользователя', blank=True, null=True)
    img = models.ImageField(upload_to='user_images/%Y/%m', verbose_name='Фото пользователя', blank=True, null=True)

    def __str__(self):
        return self.username

class TelegramOrderMessage(models.Model):
    class Meta:  
        verbose_name_plural = "Телеграмм"
    bot_token = models.CharField('Токен бота', max_length=100)
    chat_id = models.CharField('Id группы', max_length=100)
    message = models.TextField('Сообщение')

    def __str__(self):
        return self.bot_token


