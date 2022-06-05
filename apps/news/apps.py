from django.apps import AppConfig


class NewsConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name: str = "Новости"
