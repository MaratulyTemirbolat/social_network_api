from translate import Translator

from django.db import models
from django.utils.text import slugify

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class Group(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=100,
        verbose_name="Название группы"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="URL (на группу)",
        help_text="URL для поиска группы (будет в нижнем регистре)"
    )
    followers = models.ManyToManyField(
        to=CustomUser,
        blank=True,
        related_name="followed_groups",
        verbose_name="Подписчики"
    )
    members_rights = models.ManyToManyField(
        to=CustomUser,
        through="GroupAdministration",
        through_fields=("group", "user"),
        related_name="groups_rights",
        verbose_name="Позиция в группе"
    )

    class Meta:  # noqa
        verbose_name = "Группа (Сообщество)"
        verbose_name_plural = "Группы (Сообщества)"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'Группа "{self.name}"'

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = self.slug.lower()
        return super().save(*args, **kwargs)


class Privilege(AbstractDateTime):  # noqa
    MAX_PRIVILEGE_NAME = 50
    name_en = models.CharField(
        max_length=MAX_PRIVILEGE_NAME,
        unique=True,
        db_index=True,
        verbose_name="Наименование на английском"
    )
    name_ru = models.CharField(
        max_length=MAX_PRIVILEGE_NAME,
        unique=True,
        blank=True,
        db_index=True,
        verbose_name="Наименование на русском"
    )
    slug = models.SlugField(
        max_length=MAX_PRIVILEGE_NAME,
        unique=True,
        db_index=True,
        blank=True,
        verbose_name="URL (shared link)",
        help_text="URL для поиска привилегий по названию"
    )

    class Meta:  # noqa
        verbose_name = "Привилегия (В группе)"
        verbose_name_plural = "Привилегии (В группах)"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'Привилегия {self.name_ru}'

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        # translation to russian
        translator = Translator(to_lang="ru")
        self.name_ru = translator.translate(self.name_en)
        # slug part
        self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class Role(AbstractDateTime):  # noqa
    MAX_POSITION_NAME = 50
    name = models.CharField(
        verbose_name="Наименование",
        unique=True,
        db_index=True,
        max_length=MAX_POSITION_NAME
    )
    slug = models.SlugField(
        max_length=MAX_POSITION_NAME,
        unique=True,
        db_index=True,
        verbose_name="Url",
        help_text="URL для поиска роли по наименованию"
    )
    privileges = models.ManyToManyField(
        to=Privilege,
        related_name="positions"
    )

    class Meta:  # noqa
        verbose_name = "Роль (в группе)"
        verbose_name_plural = "Роли (в группе)"
        ordering = (
            'datetime_created',
        )

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f'Роль {self.name}'


class GroupAdministration(AbstractDateTime):  # noqa
    group = models.ForeignKey(
        to=Group,
        on_delete=models.RESTRICT,
        verbose_name="Группа"
    )
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        verbose_name="Пользователь группы"
    )
    role = models.ForeignKey(
        to=Role,
        on_delete=models.RESTRICT,
        verbose_name="Роль"
    )

    class Meta:  # noqa
        verbose_name = "Роль пользователя в группе"
        verbose_name_plural = "Роли пользователей в группах"
        ordering = (
            "id",
        )
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'user', 'role'],
                name="unique_group_user_role"
            ),
        ]

    def __str__(self) -> str:  # noqa
        return f"{self.user} {self.group} имеет {self.role}"
