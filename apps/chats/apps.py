from django.apps import AppConfig


class ChatsConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'
    verbose_name: str = "Чаты"
