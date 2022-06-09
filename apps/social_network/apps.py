from django.apps import AppConfig


class SocialNetworkConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_network'
    verbose_name: str = "Социальная сеть"
