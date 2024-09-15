from rest_framework import serializers
from apps.products.models import Orders

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'user_id', 'cart_id', 'delivery_method', 'delivery_address', 'recipient_phone',
                  'comments', 'status', 'total_price', 'created_at']

