from django.apps import AppConfig


class GroupsConfig(AppConfig):  # noqa
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'groups'
    verbose_name: str = "Группы и привилегии в них"
