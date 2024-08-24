from django.urls import path
from api.account.views import UserAccountUpdateView, ChangePasswordView, \
     ConfirmUserEmailView, ActivateEmailUserView, SendCodeAgainView

urlpatterns = [
    path("user/update/<int:pk>", UserAccountUpdateView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("confirm/email/", ConfirmUserEmailView.as_view()),
    path("activate/email/", ActivateEmailUserView.as_view()),
    path("send/code/again/", SendCodeAgainView.as_view()),
]