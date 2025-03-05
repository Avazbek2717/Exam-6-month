from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.common.models import News, Subscriber

@shared_task
def send_newsletter(news_id):
    try:
        news = News.objects.get(id=news_id)
        subscribers = Subscriber.objects.filter(is_active=True)

        subject = news.title
        from_email = 'toshtonovavazbek070@gmail.com'
        recipient_list = [subscriber.email for subscriber in subscribers]

        if recipient_list:
            # 📌 HTML shablon tayyorlash
            html_content = render_to_string('templates/emails/newsletter.html', {'news': news})
            text_content = strip_tags(html_content)  # Oddiy matn versiyasi

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,  # Matnli versiya
                from_email=from_email,
                to=[],  # "To" bo'sh bo'lishi kerak
                bcc=recipient_list  # Ko‘rinmas qabul qiluvchilar
            )

            email.attach_alternative(html_content, "text/html")  # HTML versiyani qo‘shish
            email.send()

        return f"News '{news.title}' sent to {len(recipient_list)} subscribers."

    except News.DoesNotExist:
        return "News not found."
