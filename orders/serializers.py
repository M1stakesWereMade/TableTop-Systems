from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']
        