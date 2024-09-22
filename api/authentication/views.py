import datetime
import random
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from api.authentication.serializers import CodeResetPasswordSerializer, ResetPasswordConfirmSerializer, \
    UserRegisterSerializer, \
    EmailCheckSerializer, CustomTokenObtainSerializer, PasswordResetSerializer, UserGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_str as force_text
from apps.user.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from api.authentication.utils import send_email_code, send_email_code_for_reset
from django.utils.translation import gettext as _
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


class ResetPasswordApiView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
                user.code = urlsafe_base64_encode(force_bytes(code))
                user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)

                user.save()
                if user.is_confirm:
                    send_email_code_for_reset(email, code)
                else:
                    send_email_code(email, code)

                return Response({'info': _('Отправлен код на указанную почту! Если не видите то проверьте спам.')},
                                status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'info': _('Если аккаунт с такой почтой существует, на почту будет отправлен код')},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeResetPasswordApiView(APIView):
    """ Активация полученного кода"""
    serializer_class = CodeResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        code = serializer.validated_data.get("code")
        email = serializer.validated_data.get("email")
        encoded = urlsafe_base64_encode(force_bytes(code))
        user = User.objects.filter(email=email, code=encoded)
        if not user.exists():
            return Response(
                {"info": _("Вы ввели неверный код.")}, status=status.HTTP_404_NOT_FOUND
            )
        user = user.first()
        user.is_confirm = True
        user.save()

        token = MyTokenObtainPairSerializer()
        tokens = token.get_token(user=user)
        data = {
            "tokens": tokens,
            "info": _("Код активирован")
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmApiView(APIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            # Использование токена для идентификации пользователя
            user = request.user
            if not user:
                return Response({"info": _("Неверный токен")}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"info": _("Пароль успешно изменен")}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
