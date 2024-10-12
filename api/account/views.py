from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import datetime
import random
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _
from api.account.serializers import UserAccountSerializer, ChangePasswordSerializer, \
    ConfirmUserEmailSerializer, ActivateUserEmailSerializer, PrivacySerializer, PolicySerializer
from api.account.utils import send_code_email_confirm
from apps.user.models import Privacy, Policy

User = get_user_model()


class UserAccountUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'info': _('Пароль успешно изменен!')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUserEmailView(APIView):
    serializer_class = ConfirmUserEmailSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
        user.code = urlsafe_base64_encode(force_bytes(code))
        user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        user.save()

        send_code_email_confirm(user.email, code)

        return Response({'info': _('Код отправлен на ваш email.')}, status=status.HTTP_200_OK)


class SendCodeAgainView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
        user.code = urlsafe_base64_encode(force_bytes(code))
        user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        user.save()

        send_code_email_confirm(user.email, code)
        return Response({"info": _("Код отправлен на ваш email.")}, status=status.HTTP_200_OK)


class ActivateEmailUserView(APIView):
    serializer_class = ActivateUserEmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        code = serializer.validated_data.get("code")
        encoded = urlsafe_base64_encode(force_bytes(code))

        if not encoded == user.code:
            return Response(
                {"info": _("Вы ввели неверный код.")}, status=status.HTTP_404_NOT_FOUND
            )

        user.is_confirm = True
        user.save()

        return Response(
            {"info": _("Email подтвержден!.")},
            status=status.HTTP_200_OK,
        )


@extend_schema_view(
    post=extend_schema(
        description=_('URL для политики'),
        summary=_('Отобразить политику конфиденциальности'),
    ),
)
class PolicyView(APIView):
    serializer_class = PolicySerializer
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Policy.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        description=_('URL для правила'),
        summary=_('Отобразить правила'),
    ),
)
class PrivacyView(APIView):
    serializer_class = PrivacySerializer
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Privacy.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)
