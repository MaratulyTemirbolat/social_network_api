from django.apps import AppConfig


class AuthsConfig(AppConfig):  # noqa
    name = 'auths'
    verbose_name: str = "Авторизация"

    def ready(self) -> None:  # noqa
        import auths.signals  # noqa
