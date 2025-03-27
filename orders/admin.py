from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Конфигурация административного интерфейса для модели Order.
    
    Attributes:
        list_display (tuple): Поля, отображаемые в списке заказов
        list_filter (tuple): Фильтры, доступные в интерфейсе
        search_fields (tuple): Поля, по которым доступен поиск
    """
    list_display = ('id', 'table_number', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('table_number',)
