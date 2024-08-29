from django.urls import path

from api.products.views import CategoryDetail

urlpatterns = [
    path('category/detail/<int:pk>', CategoryDetail.as_view()),
]