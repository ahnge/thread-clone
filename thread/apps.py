from django.apps import AppConfig


class ThreadConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "thread"

    def ready(self):
        from . import signals
