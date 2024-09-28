from rest_framework import serializers
from django.conf import settings
from apps.category.models import Category
from apps.products.models import Product, Cart, CartItems
from apps.orders.models import Order


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_id', 'description', 'images', 'price', 'weight', 'created_at']

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

        # Проверяем, существует ли товар с таким же product_id в корзине
        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity')

        try:
            # Ищем товар в корзине
            cart_item = CartItems.objects.get(cart_id=cart, product_id=product_id)
            # Увеличиваем количество существующего товара
            cart_item.quantity += quantity
            cart_item.total_item_price = cart_item.quantity * cart_item.price
            cart_item.save()

        except CartItems.DoesNotExist:
            # Если товара нет в корзине, создаем новый элемент
            cart_item = CartItems.objects.create(cart_id=cart, **validated_data)
            cart_item.price = cart_item.product_id.price
            cart_item.total_item_price = cart_item.quantity * cart_item.price
            cart_item.save()

        return cart_item


class CartItemShowSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'product_name', 'weight', 'quantity', 'image', 'price', 'total_item_price']

    def get_weight(self, obj):
        return obj.product_id.weight if obj.product_id else None

    def get_product_name(self, obj):
        return obj.product_id.name if obj.product_id else None

    def get_image(self, obj):
        if obj.product_id and obj.product_id.productimages.exists():
            return obj.product_id.productimages.first().image.url
        return None


class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemShowSerializer(many=True, read_only=True)
    total_cart_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_cart_price', 'cartitems']


class CartItemCountSerializer(CartSerializer):
    total_cart_items = serializers.SerializerMethodField()

    class Meta(CartSerializer.Meta):
        fields = ['total_cart_items']

    def get_total_cart_items(self, obj):
        # Возвращаем количество элементов в корзине
        return obj.cartitems.count()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'cart_id', 'delivery_method', 'delivery_address', 'recipient_phone', 'comments', 'status', 'total_price', 'created_at']


