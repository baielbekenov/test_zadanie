from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.category.serializers import CategorySerializer
from apps.category.models import Category


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get(self, request):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

