from django.test import TestCase
from django.urls import reverse
from .models import Order

class OrderTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        Order.objects.create(
            table_number=1,
            items=[{"name": "Пицца", "price": 500}],
            status='pending'
        )
        Order.objects.create(
            table_number=2,
            items=[{"name": "Кофе", "price": 150}],
            status='paid'
        )
        
        # Вычисляем ожидаемую выручку
        self.total_revenue = 150  # Сумма только оплаченных заказов (150 руб.)

    def test_order_creation(self):
        """Тест создания заказа."""
        order = Order.objects.get(table_number=1)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_price, 500)

    def test_revenue_calculation(self):
        """Тест расчета выручки."""
        response = self.client.get(reverse('revenue_report'))
        self.assertContains(response, f'{self.total_revenue} ₽')

    def test_order_list(self):
        """Тест отображения списка заказов."""
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Стол')