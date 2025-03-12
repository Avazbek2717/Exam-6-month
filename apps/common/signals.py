from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .utils import send_latest_notification  # Yuqorida yozgan util funksiyamiz

@receiver(post_save, sender=Notification)
def send_notification_on_create(sender, instance, created, **kwargs):
    if created:  # Faqat yangi yaratilgan bildirshnomalar uchun
        send_latest_notification()

