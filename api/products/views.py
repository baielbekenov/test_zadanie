from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.products.serializers import ProductListInCategorySerializer, ProductListSerializer, CartSerializer, \
    CartItemSerializer, ProductSerializer
from django.db import IntegrityError
from apps.category.models import Category
from apps.products.models import Product, Cart, CartItems


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """
        Переопределение метода для фильтрации по названию товара
        """
        queryset = Product.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Переопределение метода list для оборачивания ответа в ключ 'result'
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        description='API для просмотра продуктов по категориям',
        summary='Смотреть продукты согласно категории'
    ),
)
@method_decorator(cache_page(60 * 5), name='get')
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


@extend_schema_view(
    get=extend_schema(
        description='API для просмотра продукта детально',
        summary='Смотреть детально продукт'
    ),
)
@method_decorator(cache_page(60 * 3), name='retrieve')
class ProductDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Product.DoesNotExist:
            return Response({"info": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    post=extend_schema(
        description='API для создание и добавление в корзину',
        summary='Добавить в корзину'
    ),
)
class CartItemCreateView(CreateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user_id=self.request.user)
        serializer.save(cart_id=cart)
        cart.save()


@extend_schema_view(
    post=extend_schema(
        description='API для удаление продукта из корзины',
        summary='Удалить продукт из корзины'
    ),
)
class CartItemDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        deletion_cart_item = CartItems.objects.filter(id=pk).first()
        if not deletion_cart_item:
            return Response({"message": "Нет такого обьекта"}, status=status.HTTP_404_NOT_FOUND)
        deletion_cart_item.quantity -= 1
        if deletion_cart_item.quantity <= 0:
            deletion_cart_item.delete()
            return Response({"message": "Товар удален из корзины, количество стало 0"}, status=status.HTTP_200_OK)
        deletion_cart_item.total_item_price = deletion_cart_item.quantity * deletion_cart_item.price
        deletion_cart_item.save()

        cart = deletion_cart_item.cart_id
        cart.total_cart_price = cart.calculate_total_price()
        cart.save()
        return Response({"message": "Количество товара уменьшено"}, status=status.HTTP_200_OK)



@extend_schema_view(
    get=extend_schema(
        description='API для просмотра корзины',
        summary='Смотреть содержимое корзины'
    ),
)
class CartView(APIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = Cart.objects.filter(user_id=self.request.user).order_by('created_at')
        serializer = self.serializer_class(cart, many=True, context={'request': request})
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        description='API для очищение корзины',
        summary='Очистить корзину'
    ),
)
class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user_id=request.user).first()
        if not cart:
            return Response({"message": "Корзина не найдена"}, status=status.HTTP_404_NOT_FOUND)

        CartItems.objects.filter(cart_id=cart).delete()
        cart.total_cart_price = 0
        cart.save()
        return Response({"message": "Корзина очищена"}, status=status.HTTP_204_NO_CONTENT)









