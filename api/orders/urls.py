from django.urls import path
from api.orders.views import CreateOrderView, UpdateOrderStatusView

urlpatterns = [
    path('order/create/', CreateOrderView.as_view(), name='create-order'),
    path('order/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]