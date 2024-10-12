from django.urls import path

from api.category.views import CategoryListView, BannerListView
from api.products.views import CategoryDetail

urlpatterns = [
    path('category/list/', CategoryListView.as_view()),
    path('banner/list/', BannerListView.as_view())
]


