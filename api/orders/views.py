from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.products.models import Orders, Cart
from api.products.serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получаем корзину пользователя
        cart = Cart.objects.filter(user_id=request.user).first()

        if not cart or cart.cartitems.count() == 0:
            return Response({"error": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        # Собираем данные для заказа
        order_data = {
            'user_id': request.user.id,
            'cart_id': cart.id,
            'delivery_method': request.data.get('delivery_method'),
            'delivery_address': request.data.get('delivery_address'),
            'recipient_phone': request.data.get('recipient_phone'),
            'comments': request.data.get('comments', ''),
            'status': 'Ожидает оплаты',  # Начальный статус заказа
            'total_price': cart.total_cart_price,  # Итоговая цена — общая стоимость корзины
        }

        # Сериализуем данные заказа
        serializer = OrderSerializer(data=order_data)

        if serializer.is_valid():
            order = serializer.save()

            # После успешного создания заказа возвращаем информацию
            return Response({"message": "Заказ создан", "order_id": order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            # Находим заказ
            order = Orders.objects.get(id=order_id, user_id=request.user)

            # Обновляем статус заказа после успешной оплаты
            order.status = 'Оплачено'
            order.save()

            return Response({"message": "Статус заказа обновлен на 'Оплачено'"}, status=status.HTTP_200_OK)

        except Orders.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)