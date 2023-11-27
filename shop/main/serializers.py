from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

from django.db.models import Q





from .models import *

from datetime import datetime
import re

User = get_user_model()

class PlantsSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField('get_category')
   

    def get_category(self, obj):
        return obj.category.cat_name

    class Meta:
        model = Plant
        
        fields = [
            'id',
            'plant_name',
            'price',
			'old_price',
            'short_description',
            'full_description',
            'main_img',
            'category'
		]
        
class OrdersSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    plants = serializers.SlugRelatedField(queryset=Plant.objects.all(),slug_field='plant_name',many=True)
    
    class Meta:
        model = Order
        fields = [
        'id',
        'user',
        'first_name' ,
        'last_name' ,
        'email',
        'address' ,
        'city' ,
        'created',
        'plants' ,
        'telegram_name',
        'phone_number',
		]


    def validate_address(self,address):
        if len(address) < 10:
            raise ValidationError('Минимальная длина адреса 10 символов')
        return address

    def validate_telegram_name(self, telegram_name):
        if telegram_name[0] != '@':
            raise ValidationError('Ник должен содержать символ @')
        if len(telegram_name) < 5:
            raise ValidationError('Минимальная длина ника 5 символов')
        return telegram_name
    
    def validate_email(self,email):
        try:
            print(email)
            user = User.objects.get(email=email)
            print(user)
            return email

        except User.DoesNotExist:
            raise ValidationError('Такой почты не существует в базе!')
