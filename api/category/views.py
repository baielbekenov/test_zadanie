from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.category.serializers import CategorySerializer, AppBarSerializer
from apps.category.models import Category, AppBar


class AppBarListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AppBarSerializer

    def get(self, request):
        appbar = AppBar.objects.all()
        serializer = self.serializer_class(appbar, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get(self, request):
        category = Category.objects.all()
        serializer = self.serializer_class(category, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

