from rest_framework import serializers
from django.conf import settings
from apps.category.models import Category
from apps.products.models import Product, Cart, CartItems, Orders


class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'weight', 'images', 'description']

    def get_images(self, obj):
        request = self.context.get('request')
        first_image = obj.productimages.first()
        if first_image:
            image_url = first_image.image.url
            if request is not None:
                return request.build_absolute_uri(image_url)
            else:
                return settings.MEDIA_URL + image_url
        else:
            default_image = request.build_absolute_uri('/media/')
            return default_image


class ProductListInCategorySerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=True, read_only=True, source='productcategory')

    class Meta:
        model = Category
        fields = ['id', 'name',  'product']


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_item_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItems
        # Убираем cart_id из полей, так как он будет привязан автоматически
        fields = ['id', 'product_id', 'quantity', 'price', 'total_item_price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть положительным.")
        if value > 2147483647:  # Ограничение для INT в базе данных
            raise serializers.ValidationError("Количество слишком велико.")
        return value

    def create(self, validated_data):
        # Получаем или создаем корзину для текущего пользователя
        cart, created = Cart.objects.get_or_create(user_id=self.context['request'].user)

        # Убираем cart_id из validated_data, если оно там есть
        validated_data.pop('cart_id', None)

        # Создаем объект CartItems с привязкой к корзине
        cart_item = CartItems.objects.create(cart_id=cart, **validated_data)

        # Рассчитываем цену и общую стоимость
        cart_item.price = cart_item.product_id.price
        cart_item.total_item_price = cart_item.quantity * cart_item.price
        cart_item.save()

        return cart_item


class CartItemShowSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price', 'total_item_price']

    def get_product_name(self, obj):
        return obj.product_id.name if obj.product_id else None


class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemShowSerializer(many=True, read_only=True)
    total_cart_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_cart_price', 'cartitems']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'user_id', 'cart_id', 'delivery_method', 'delivery_address', 'recipient_phone', 'comments', 'status', 'total_price', 'created_at']


