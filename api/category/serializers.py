from rest_framework import serializers

from apps.category.models import Category, AppBar


class AppBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppBar
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']