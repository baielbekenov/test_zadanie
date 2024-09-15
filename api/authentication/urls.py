from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.authentication.views import (UserRegisterApiView,
                                      CustomTokenObtainView,
                                      ResetPasswordApiView, ResetPasswordConfirmApiView, CodeResetPasswordApiView,
                                      GetMeApiView)

urlpatterns = [
    path("login/", CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("users/me/", GetMeApiView.as_view()),
    path("register/", UserRegisterApiView.as_view()),

    path("reset/password/", ResetPasswordApiView.as_view()),
    path("reset/code/confirm/", CodeResetPasswordApiView.as_view()),
    path("reset/password/confirm/", ResetPasswordConfirmApiView.as_view())
]