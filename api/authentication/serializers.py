from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings

from apps.user.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField(write_only=True)

    default_error_messages = {
        "no_active_account": "Неправильный логин или пароль"
    }

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        user = authenticate(request=self.context.get('request'), phone=phone, password=password)
        if not user:
            raise serializers.ValidationError(self.error_messages["no_active_account"], code="no active account")
        refresh = self.get_token(user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['user'] = {
            'id': user.id,
            'phone': user.phone,
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = user.phone
        return token


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20, required=False)
    phone = serializers.CharField(max_length=15, required=False)
    password1 = serializers.CharField()
    email = serializers.EmailField()

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1

    def validate_email(self, email):
        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже зарегистрирован."
            )
        return email

    def validate_phone(self, phone):
        if User.objects.filter(phone=phone, is_active=True).exists():
            raise serializers.ValidationError(
                "Пользователь с таким номером телефона уже зарегистрирован."
            )
        return phone

    class Meta:
        model = User
        fields = ("phone", "password1", 'email')
