from django.urls import path

from api.products.views import CategoryDetail, ProductDetailView, CartItemCreateView, CartItemDeleteView, CartView, \
    CartClearView, ProductSearchView

urlpatterns = [
    path('category/detail/<int:pk>', CategoryDetail.as_view()),
    path('detail/<int:pk>', ProductDetailView.as_view()),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),

    path('cart/add-item/', CartItemCreateView.as_view(), name='cart-add-item'),
    path('delete/cart/item/<int:pk>', CartItemDeleteView.as_view()),
    path('cart/clear/', CartClearView.as_view()),
    path('cartview/', CartView.as_view()),
]