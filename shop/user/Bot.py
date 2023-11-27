import requests
from django.http import HttpResponse

from main.models import OrderItem
from .models import *


from datetime import datetime


from datetime import datetime

def sendMessageTg(order_item):
    try:
        if TelegramOrderMessage.objects.get(pk=1):
            tg_data = TelegramOrderMessage.objects.get(pk=1)
            token = str(tg_data.bot_token)
            chat_id = str(tg_data.chat_id)
            text = str(tg_data.message)

            order = order_item  # Получение объекта заказа

            order_items = OrderItem.objects.filter(order=order)  # Получение всех OrderItem для текущего заказа

            order_items_text = ""  # Переменная для хранения текста всех OrderItem

            # Формирование текста для каждого OrderItem
            for item in order_items:
                item_data = {
                    'Название товара': item.plant.plant_name,
                    'Цена': item.price,
                    'Кол-во': item.quantity,
                    'Время создания': item.time_created.strftime('%Y-%m-%d %H:%M'),  # Форматирование времени создания
                    'Общая цена за позицию': item.get_cost(),
                }

                item_text = ""  # Переменная для хранения текста одного OrderItem

                # Формирование текста одного OrderItem
                for field_name, field_value in item_data.items():
                    item_text += f"{field_name}: {field_value}\n"

                order_items_text += item_text + "\n"  # Добавление текста одного OrderItem к общему тексту всех OrderItem





            # Формирование сообщения с использованием всех полей модели Order
            for field in order._meta.fields:
                field_name = field.name
                field_value = getattr(order, field_name)


                if field_value:
                    if isinstance(field_value, datetime):
                        field_value = field_value.strftime('%Y-%m-%d %H:%M')  # Форматирование времени

                    text = text.replace(f'{{{{ {field_name} }}}}', str(field_value))
            get_total_cost = order.get_total_cost()
            # Добавление текста всех OrderItem к сообщению
            text = text.replace("{{ order_items }}", order_items_text)
            text  = text.replace("{{ get_total_cost }}", str(get_total_cost))
            url_req = f"https://api.telegram.org/{token}/sendMessage?chat_id={chat_id}&text={text}"
            results = requests.get(url_req)
    except:
        return HttpResponse('<h1>Ошибка сервера</h1>')


