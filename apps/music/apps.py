from django.apps import AppConfig


class MusicConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'
    verbose_name: str = "Музыка"
