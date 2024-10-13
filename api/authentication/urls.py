from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from api.authentication.views import (UserRegisterApiView,
                                      CustomTokenObtainView,
                                      GetMeApiView, websocket_view)


urlpatterns = [
    path("register/", UserRegisterApiView.as_view()),
    path("login/", CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/me/", GetMeApiView.as_view()),

    path('websocket', websocket_view, name='websocket_view'),
]