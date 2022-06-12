from django.apps import AppConfig


class ComplainsConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'complains'
    verbose_name: str = "Жалобы"
