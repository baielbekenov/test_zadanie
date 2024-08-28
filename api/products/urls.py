from django.urls import path

from api.products.views import CategoryDetail, CategoryListView

urlpatterns = [
    path('category/list/', CategoryListView.as_view()),
    path('category/detail/<int:pk>', CategoryDetail.as_view()),
]