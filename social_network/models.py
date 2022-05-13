from argparse import ONE_OR_MORE
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
        max_length=MAX_PRIVILEGE_NAME
    )


class Position(AbstractDateTime):  # noqa
    MAX_POSITION_NAME = 50
    name = models.CharField(
        verbose_name="Наименование",
        max_length=MAX_POSITION_NAME
    )
    privileges = models.ManyToManyField(
        to=Privilege,
        related_name="positions"
    )


class ComplainReason(AbstractDateTime):  # noqa
    MAX_COMPLAIN_NAME = 100
    name = models.CharField(
        max_length=MAX_COMPLAIN_NAME,
        verbose_name="Наименование"
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
