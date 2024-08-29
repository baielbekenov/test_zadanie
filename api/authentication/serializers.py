from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings

from apps.user.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField(write_only=True)

    default_error_messages = {
        "no_active_account": _("Неправильный логин или пароль")
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

        # Дополнительная информация о пользователе
        data['user'] = {
            'id': user.id,
            'phone': user.phone,
            # добавьте любые другие необходимые поля
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # добавьте в токен дополнительные клеймы
        token['phone'] = user.phone
        return token



class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=False)
    password1 = serializers.CharField()
    email = serializers.EmailField()

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1

    def validate_email(self, email):
        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError(
                _("Пользователь с такой почтой уже зарегистрирован.")
            )
        return email

    def validate_phone(self, phone):
        if User.objects.filter(phone=phone, is_active=True).exists():
            raise serializers.ValidationError(
                _("Пользователь с таким номером телефона уже зарегистрирован.")
            )
        return phone

    class Meta:
        model = User
        fields = ("phone", "password1", 'email')


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Проверка введенного email в базе данных.
        """
        try:

            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Почты не существует!"))
        return value


class CodeResetPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    email = serializers.EmailField()

    def validate_code(self, value):
        """
        Проверять код на шестизначность чисел
        """
        if len(str(value)) != 6 or value < 0:
            raise serializers.ValidationError(_('Код должен быть шестизначным!'))
        return value


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, new_password):
        if not validate_password(new_password):
            return new_password
