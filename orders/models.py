from django.db import models
from django.core.exceptions import ValidationError
import json
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Список блюд", default=list)
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Общая стоимость", 
        blank=True, 
        null=True
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        """Проверка данных перед сохранением."""
        try:
            for item in self.items:
                if not isinstance(item.get('price'), (int, float)):
                    raise ValidationError("Цена должна быть числом.")
        except Exception as e:
            raise ValidationError(f"Ошибка в items: {str(e)}")
        
        if self.total_price is not None and self.total_price < 0:
            raise ValidationError("Общая стоимость не может быть отрицательной.") 
        
    
    @property
    def items_text(self):
        """Возвращает items в текстовом формате для формы."""
        return '\n'.join([f"{item['name']} - {item['price']}" for item in self.items])
        

    def calculate_total_price(self):
        """Рассчитывает общую стоимость заказа на основе items."""
        return sum(Decimal(str(item['price'])) for item in self.items)


    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"
    
    
    