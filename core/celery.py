import os
from celery import Celery

# Django loyihasining nomini aniqlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")


# Django settings.py dagi CELERY_ bilan boshlanadigan sozlamalarni yuklash
app.config_from_object("django.conf:settings", namespace="CELERY")

# Loyihadagi barcha app-lardagi Celery vazifalarini avtomatik yuklash
app.autodiscover_tasks()
