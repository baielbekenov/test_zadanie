import datetime
from rest_framework.views import APIView
from api.authentication.serializers import UserRegisterSerializer, CustomTokenObtainSerializer, UserGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.response import Response
from rest_framework import status
from apps.user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        refresh = super().get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data


class GetMeApiView(APIView):
    """Позволяет пользователю получить информацию о себе"""
    serializer_class = UserGetSerializer

    def get(self, request):
        user = self.request.user

        return Response(
            {
                "user": UserGetSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class UserRegisterApiView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        phone = serializer.validated_data.get("phone")
        raw_password = serializer.validated_data.get("password1")
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data.get("first_name")

        user = User.objects.filter(phone=phone)
        if user.exists():
            user = user.first()
            user.created_at = datetime.datetime.now(datetime.timezone.utc)
        else:
            user = User(
                phone=phone,
                is_confirm=False,
                first_name=first_name,
                email=email,
                created_at = datetime.datetime.now(datetime.timezone.utc)
            )

        user.set_password(raw_password)
        user.save()
        das = MyTokenObtainPairSerializer()
        tokens = das.get_token(user=user)
        data = {
            'info': "Успешно зарегистрирован!",
            "tokens": tokens
        }
        return Response(data, status=status.HTTP_200_OK)

