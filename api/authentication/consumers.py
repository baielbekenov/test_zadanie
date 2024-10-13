import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications'

        # Присоединяемся к группе уведомлений
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Отправляем приветственное сообщение после подключения
        await self.send(text_data=json.dumps({
            'message': 'Соединение установлено, вы подключены к уведомлениям!'
        }))
        print("WebSocket connection opened.")

    async def disconnect(self, close_code):
        # Отключаемся от группы уведомлений
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket connection closed with code: {close_code}")

    # Получение сообщений из группы
    async def send_notification(self, event):
        message = event['message']
        print(f"Sending notification: {message}")  # Выводим уведомление через print

        # Отправляем сообщение через WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))