from rest_framework import serializers
from apps.orders.models import Order, Coordinates, Address, Contact
from apps.products.models import CartItems


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude']


class AddressSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer()

    class Meta:
        model = Address
        fields = ['cityName', 'country', 'postalCode', 'rawAddress', 'details', 'streetName', 'streetNumber', \
                  'coordinates']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'name', 'phone']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product_id', 'quantity', 'total_item_price']


class PackageDetailSerializer(serializers.Serializer):
    contentType = serializers.CharField()
    description = serializers.CharField()
    parcelValue = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):
    delivery_address = AddressSerializer()
    pickup_address = AddressSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Order
        fields = ['delivery_address', 'pickup_address', 'contact', 'created_at']


class CreateOrderSerializer(serializers.Serializer):
    delivery_address_id = serializers.IntegerField()
    pickup_address_id = serializers.IntegerField()
    contact_id = serializers.IntegerField()

