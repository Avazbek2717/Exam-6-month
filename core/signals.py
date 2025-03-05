from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.common.models import News
from core.task import send_newsletter

@receiver(post_save, sender=News)
def send_newsletter_on_create(sender, instance, created, **kwargs):
    if created:
        send_newsletter.delay(instance.id)  # Celery ishga tushadi
