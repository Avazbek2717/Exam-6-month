from django.apps import AppConfig

class AppsConfig(AppConfig):  # Klass nomi loyihangizga mos bo'lishi kerak
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'  # Loyiha nomi shu bo'lishi kerak

    def ready(self):
        from . import signals  # Signals faylini yuklaymiz
