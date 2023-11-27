
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.urls import reverse
from datetime import datetime

from shop import settings
from simple_history.models import HistoricalRecords 

class Plant(models.Model):
    """Растение"""
    class Meta:  
        verbose_name_plural = "Растения"
    plant_name = models.CharField('Название растения', max_length=200)
    old_price = models.DecimalField(max_digits=6, decimal_places=2,
                                    verbose_name='Старая цена', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                    verbose_name='Актуальная цена')
    short_description = models.TextField('Короткое описание')
    full_description = models.TextField('Полное описание')
    main_img = models.ImageField(upload_to='images/%Y/%m',
                                 verbose_name='Главное фото растения')
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='category', verbose_name='Категория')

    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('flower-detail', args=[self.pk])

    def __str__(self):
        return self.plant_name

class Category(models.Model):
    """Категория растения"""
    class Meta:  
        verbose_name_plural = "Категории"

    cat_name = models.CharField('Название категории', max_length=100)

    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('category', args=[self.pk])

    def __str__(self):
        return self.cat_name
    



class PlantPhotos(models.Model): 
    """Галерея фото для растения""" 
    images = models.ImageField(upload_to='images/%Y/%m', verbose_name="Галерея фотографий") 
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)
    
    history = HistoricalRecords()

    class Meta:  
        verbose_name_plural = "Галерея растений"



class Order(models.Model):
    class Meta:  
        verbose_name_plural = "Заказы"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField(verbose_name='Почта')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Точный адрес')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    plants = models.ManyToManyField(Plant, through='OrderItem')
    telegram_name = models.CharField(max_length=50, verbose_name="Имя телеграм")
    phone_number = PhoneNumberField(blank=True, verbose_name='Номер телефона')
    

    history = HistoricalRecords()

    def formatted_created(self):
        return self.created.strftime('%Y-%m-%d %H:%M')

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f'Заказ - {self.pk}'

class OrderItem(models.Model):
    class Meta:  
        verbose_name_plural = "Детали заказов"

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    history = HistoricalRecords()

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f'Заказ - {self.order}'

@receiver(pre_delete, sender=Plant)
def image_model_delete(sender, instance, **kwargs):
    if instance.main_img.name:
        instance.main_img.delete(False)

@receiver(pre_delete, sender=PlantPhotos)
def image_model_delete(sender, instance, **kwargs):
    if instance.images.name:
        instance.images.delete(False)

# from django.shortcuts import render, redirect
# from .cart import Cart
# from .forms import OrderForm
# from .models import Order, OrderItem
#
