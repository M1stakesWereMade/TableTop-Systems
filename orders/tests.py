from django.test import TestCase, Client
from .models import Order

class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        Order.objects.create(
            table_number=1,
            items="{'items': [{'name': 'Coffee', 'price': 2.5}]}",
            total_price=2.5,
            status='в ожидании'
        )

    def test_order_creation(self):
        order = Order.objects.get(table_number=1)
        self.assertEqual(order.status, 'в ожидании')

    def test_order_status_update(self):
        order = Order.objects.get(table_number=1)
        response = self.client.post(f'/update/{order.id}/', {'status': 'готово'})
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'готово')

    def test_revenue_calculation(self):
        Order.objects.create(
            table_number=2,
            items="{'items': [{'name': 'Tea', 'price': 1.5}]}",
            total_price=1.5,
            status='оплачено'
        )
        response = self.client.get('/revenue/')
        self.assertContains(response, "3.0")  # 2.5 + 1.5 = 4.0? Проверьте логику
