from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.products.serializers import ProductListInCategorySerializer, ProductListSerializer, CategorySerializer
from apps.category.models import Category
from apps.products.models import Product


class CategoryDetail(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductListInCategorySerializer

    def get(self, request, pk, format=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")

        product = Product.objects.filter(category_id=category)
        product_serializer = ProductListSerializer(product, many=True, context={'request': request})

        category_serializer = self.serializer_class(category, context={'request': request})
        data = category_serializer.data
        data['products'] = product_serializer.data

        return Response({"result": data}, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get(self, request):
        category = Category.objects.all()
        serializer = self.serializer_class(category, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

