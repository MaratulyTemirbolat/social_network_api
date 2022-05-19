from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class Phone(AbstractDateTime):  # noqa
    phone = models.CharField(
        max_length=12,
        verbose_name="Номер телефона"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        verbose_name="Владелец",
        related_name="phones"
    )


class Chat(AbstractDateTime):  # noqa
    is_group = models.BooleanField(
        verbose_name="Группа",
        default=False
    )
    photo = models.ImageField(
        upload_to='chat/photos/%Y/%m/%d/',
        blank=True,
        verbose_name='Миниатюра'
    )

    class Meta:  # noqa
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ["-datetime_updated"]


class Message(AbstractDateTime):  # noqa
    content = models.TextField(
        verbose_name="Конент"
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.RESTRICT,
        related_name="messages",
        verbose_name="Чат"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="messages",
        verbose_name="Владелец"
    )

    class Meta:  # noqa
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-datetime_created"]


class Privilege(AbstractDateTime):  # noqa
    MAX_PRIVILEGE_NAME = 50
    name = models.CharField(
        verbose_name="Наименование",
        unique=True,
        max_length=MAX_PRIVILEGE_NAME
    )


class Position(AbstractDateTime):  # noqa
    MAX_POSITION_NAME = 50
    name = models.CharField(
        verbose_name="Наименование",
        unique=True,
        max_length=MAX_POSITION_NAME
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )
    privileges = models.ManyToManyField(
        to=Privilege,
        related_name="positions"
    )


class ComplainReason(AbstractDateTime):  # noqa
    MAX_COMPLAIN_NAME = 100
    name = models.CharField(
        max_length=MAX_COMPLAIN_NAME,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


class Complain(AbstractDateTime):  # noqa
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name='complains',
        verbose_name="Владелец жалобы"
    )
    reason = models.ForeignKey(
        to=ComplainReason,
        on_delete=models.RESTRICT,
        related_name="complains",
        verbose_name="Причина жалобы"
    )
    content = models.TextField(
        verbose_name="Текст"
    )


class Tag(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


class Category(AbstractDateTime):  # noqa
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


class Group(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=100,
        verbose_name="Название группы"
    )
    followers = models.ManyToManyField(
        to=CustomUser,
        related_name="groups",
        blank=True
    )
    members_rights = models.ManyToManyField(
        to=CustomUser,
        through="GroupAdministration",
        through_fields=("user", "group"),
        related_name="group_rights"
    )


class GroupAdministration(AbstractDateTime):  # noqa
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        verbose_name="Пользователь группы"
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.RESTRICT,
        verbose_name="Группа"
    )
    position = models.ForeignKey(
        to=Position,
        on_delete=models.RESTRICT,
        verbose_name="Статус"
    )
