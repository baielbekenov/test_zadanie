from django.urls import path
from api.authentication import consumers

urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),  # Пример WebSocket маршрута
]