from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification  # Modelni import qilamiz

def send_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)  # Modeldan ma'lumotni olamiz
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications_group",
            {
                "type": "send_notification",
                "title": notification.title,
                "body": notification.body,
                "image_url": notification.image.url if notification.image else None,
                "url": notification.url
            }
        )
    except Notification.DoesNotExist:
        print("Notification not found")
