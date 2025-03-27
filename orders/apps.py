from django.apps import AppConfig

class OrdersConfig(AppConfig):
    """
    Конфигурация приложения 'orders'.
    
    Attributes:
        default_auto_field (str): Тип автоинкрементного поля по умолчанию
        name (str): Название приложения
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
