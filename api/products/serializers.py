from rest_framework import serializers
from django.conf import settings

from apps.category.models import Category
from apps.products.models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


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

