from django.apps import AppConfig


class LocationsConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locations'
    verbose_name: str = "Локации"
