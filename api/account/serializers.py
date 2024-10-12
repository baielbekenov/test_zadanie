from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from apps.user.models import Policy, Privacy

User = get_user_model()


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone']


class ConfirmUserEmailSerializer(serializers.Serializer):
    is_confirm = serializers.BooleanField(required=True)


class ActivateUserEmailSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        try:
            password_validation.validate_password(value, user)
        except ValidationError as e:
            custom_errors = []
            for error in e.messages:
                if "This password is too short." in error:
                    custom_errors.append("Пароль слишком короткий. Он должен содержать как минимум 8 символов.")
                else:
                    custom_errors.append("Этот пароль слишком распространён")
            raise serializers.ValidationError(custom_errors)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['title', 'text']


class PrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Privacy
        fields = ['title', 'text']