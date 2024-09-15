from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.products.serializers import ProductListInCategorySerializer, ProductListSerializer, CartSerializer, \
    CartItemSerializer
from django.db import IntegrityError
from apps.category.models import Category
from apps.products.models import Product, Cart, CartItems


class CategoryDetail(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListInCategorySerializer

    def get(self, request, pk, format=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")

        product = Product.objects.filter(category_id=category)
        product_serializer = ProductListSerializer(product, many=True, context={'request': request})

        category_serializer = self.serializer_class(category, context={'request': request})
        data = category_serializer.data
        data['products'] = product_serializer.data

        return Response({"result": data}, status=status.HTTP_200_OK)


class ProductDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'pk'

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"info": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)


class CartItemCreateView(CreateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user_id=self.request.user)
        serializer.save(cart_id=cart)
        cart.save()


class CartItemDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        deletion_cart_item = CartItems.objects.filter(id=pk)
        if not deletion_cart_item.exists():
            return Response({"message": "Нет такого обьекта"}, status=status.HTTP_404_NOT_FOUND)
        cart = deletion_cart_item.first().cart_id
        deletion_cart_item.delete()
        cart.total_cart_price = cart.calculate_total_price()
        cart.save()
        return Response({"message": "Обьект удален"}, status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = Cart.objects.filter(user_id=self.request.user)
        serializer = self.serializer_class(cart, many=True, context={'request': request})
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)









