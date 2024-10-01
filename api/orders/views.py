from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.orders.serializers import AddressSerializer, ContactSerializer, PackageDetailSerializer, CreateOrderSerializer
from api.orders.utils import find_nearest_pickup_point
from apps.products.models import Cart, CartItems
from api.products.serializers import OrderSerializer
from apps.orders.models import Order, Address, Contact


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Получаем данные корзины
        try:
            cart = Cart.objects.get(user_id=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем данные для доставки и контакта
        delivery_address_id = serializer.validated_data.get("delivery_address_id")
        contact_id = serializer.validated_data.get('contact_id')

        try:
            delivery_address = Address.objects.get(id=delivery_address_id)
            contact = Contact.objects.get(id=contact_id)
        except (Address.DoesNotExist, Contact.DoesNotExist):
            return Response({"error": "Invalid delivery or contact details"}, status=status.HTTP_400_BAD_REQUEST)

        nearest_pickup_point = find_nearest_pickup_point(delivery_address)
        if not nearest_pickup_point:
            return Response({"error": "No available pickup points"}, status=status.HTTP_400_BAD_REQUEST)

        # Создание заказа
        order = Order.objects.create(cart_id=cart, delivery_address=delivery_address, pickup_address=nearest_pickup_point, contact=contact)

        # Формирование деталей посылки из товаров в корзине
        cart_items = CartItems.objects.filter(cart_id=cart)
        description = ", ".join([f"{item.quantity}x {item.product_id.name}" for item in cart_items])
        parcel_value = sum([item.total_item_price for item in cart_items])
        weight = sum([item.product_id.weight for item in cart_items])
        print('description ', description)
        print('parcel_value ', parcel_value)
        print('weight ', weight)

        package_details = {
            "contentType": "FOOD",
            "description": description,
            "parcelValue": parcel_value,
            "weight": weight
        }
        package_serializer = PackageDetailSerializer(data=package_details)
        if not package_serializer.is_valid():
            return Response({"error": package_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        package_serializer = PackageDetailSerializer(data=package_details)
        if not package_serializer.is_valid():
            return Response({"error": "Invalid package details"}, status=status.HTTP_400_BAD_REQUEST)

        # Создание JSON ответа
        response_data = {
            "address": AddressSerializer(delivery_address).data,
            "contact": ContactSerializer(contact).data,
            "packageDetails": package_serializer.data,
            "packageId": f"order_{order.id}",
            "pickupDetails": {
                "address": AddressSerializer(nearest_pickup_point).data,
                "addressBook": {"id": "00000000-0000-0000-0000-000000000000"},
                "pickupOrderCode": "PickupOrderCode123",
                "pickupTime": "2019-08-24T14:15:22Z",  # Пример времени
                "pickupPhone": "+34666666666"
            },
            "price": {
                "paymentType": "CASH_ON_DELIVERY",
                "delivery": {
                    "currencyCode": "EUR",
                    "value": 5.5
                },
                "parcel": {
                    "currencyCode": "EUR",
                    "value": parcel_value
                }
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            # Находим заказ
            order = Order.objects.get(id=order_id, user_id=request.user)

            # Обновляем статус заказа после успешной оплаты
            order.status = 'Оплачено'
            order.save()

            return Response({"message": "Статус заказа обновлен на 'Оплачено'"}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)