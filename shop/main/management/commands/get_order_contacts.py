
from django.core.management.base import BaseCommand

from ...models import Order





class Command(BaseCommand):
    help = 'Получить контакты заказа по id'
    
    def add_arguments(self,parser):
        parser.add_argument(
            "order_id", nargs='+', type=int, help='Id заказа'
        )

    def handle(self,*args,**kwargs):
        order_ids = kwargs['order_id']
    
        for order_id in order_ids:
            try:
                order = Order.objects.get(pk=order_id)
                self.stdout.write(f'Телеграм и контакты заказа по id - {order_id}: "{order.first_name} {order.last_name}" {order.telegram_name}')

            except Order.DoesNotExist:
                self.stdout.write(f'Заказ с "{order_id}" не найден!')