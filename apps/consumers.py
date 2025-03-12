import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "No message")

        # WebSocket orqali kelayotgan ma'lumotni qayta yuborish
        await self.send(text_data=json.dumps({
            "message": message
        }))

    async def send_notification(self, event):
        """Bildirishnoma yuborish funksiyasi"""
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "body": event["body"],
            "image_url": event.get("image_url"),
            "url": event.get("url"),
        }))
