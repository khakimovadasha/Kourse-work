from main.models import Plant, Category
from django.test import TestCase
from main.models import Order, OrderItem, Plant
from user.models import User

class PlantTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(cat_name='Категория1')
        Plant.objects.create(
            plant_name='Цветок1',
            old_price=9.99,
            price=11.99,
            short_description='short_description',
            full_description='full_description',
            main_img='test',
            category=category
        )
        Plant.objects.create(
            plant_name='Цветок2',
            old_price=99.99,
            price=111.99,
            short_description='short_description2',
            full_description='full_description2',
            main_img='test2',
            category=category
        )

    def test_plant_is_valid(self):
        plant1 = Plant.objects.get(plant_name='Цветок1')
        plant2 = Plant.objects.get(plant_name='Цветок2')
        self.assertEqual(str(plant1), 'Цветок1')
        self.assertEqual(str(plant2), 'Цветок2')

    def test_plant_has_old_price(self):
        plant = Plant.objects.get(plant_name='Цветок1')
        self.assertIsNotNone(plant.old_price)

    def test_plant_price_greater_than_old_price(self):
        plant = Plant.objects.get(plant_name='Цветок1')
        self.assertGreater(plant.price, plant.old_price)

    def test_plant_has_category(self):
        plant = Plant.objects.get(plant_name='Цветок1')
        self.assertIsNotNone(plant.category)

    def test_plant_has_main_image(self):
        plant = Plant.objects.get(plant_name='Цветок1')
        self.assertIsNotNone(plant.main_img)


class OrderTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        category = Category.objects.create(cat_name='Категория1')
        plant = Plant.objects.create(
            plant_name='Цветок1',
            price=10.99,
            short_description='short_description',
            full_description='full_description',
            main_img='test',
            category=category
        )
        order = Order.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            telegram_name='test_telegram',
            phone_number='1234567890'
        )
        OrderItem.objects.create(
            order=order,
            plant=plant,
            price=plant.price,
            quantity=2
        )

    def test_order_exists(self):
        order_count = Order.objects.count()
        self.assertEqual(order_count, 1)

    def test_order_details(self):
        order = Order.objects.first()
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.last_name, 'Doe')
        self.assertEqual(order.email, 'test@example.com')
        self.assertEqual(order.telegram_name, 'test_telegram')
        self.assertEqual(order.phone_number, '1234567890')

    def test_order_total_cost(self):
        order = Order.objects.first()
        expected_total_cost = 2 * order.items.first().price
        self.assertEqual(order.get_total_cost(), expected_total_cost)

    def test_order_string_representation(self):
        order = Order.objects.first()
        self.assertEqual(str(order), f'Заказ - {order.pk}')

