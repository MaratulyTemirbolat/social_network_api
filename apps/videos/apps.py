from django.apps import AppConfig


class VideosConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'
    verbose_name: str = "Видео"

    def ready(self) -> None:  # noqa
        import videos.signals  # noqa
