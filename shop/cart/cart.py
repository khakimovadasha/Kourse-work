from decimal import Decimal

from django.conf import settings
from main.models import Plant
class Cart(object):
    def __init__(self,request):
        """Инициализируем объект корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID) #находим корзину по ключу
        if not cart: # если корзина пустая
            cart = self.session[settings.CART_SESSION_ID] ={}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Добавляем товар в корзину"""
        product_id = str(product.id) #именно формат "str" т.к используем json
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0, 'price':str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity']=quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Метод для сохранения"""
        self.session.modified = True

    def remove(self, product):
        """Удаляем item из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """итерация по элементам корзины"""
        product_ids = self.cart.keys()
        products = Plant.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] =product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Общее кол-во  товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())
    def get_total_price(self):
        """Общая цена товаров в корзине"""
        return sum(Decimal(item['price']) * Decimal(item['quantity']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

