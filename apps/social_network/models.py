from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


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


class Video(AbstractDateTime):  # noqa

    video_file = models.FileField(
        upload_to="documents/videos/%Y/%m/%d",
        verbose_name="Видео файл"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="owned_videos",
        verbose_name="Владелец"
    )
    keepers = models.ManyToManyField(
        to=CustomUser,
        related_name="added_videos",
        verbose_name="Имеется пользователями"
    )


class Country(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название страны"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


class City(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=100,
        verbose_name="Наименованеи города"
    )
    country = models.ForeignKey(
        to=Country,
        on_delete=models.RESTRICT,
        related_name="attached_cities",
        verbose_name="Страна"
    )


class ProfilePhoto(AbstractDateTime):  # noqa
    photo = models.ImageField(
        upload_to="photos/profile_photos/%Y/%m/%d",
        verbose_name="Фото профиля"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="profile_photos"
    )
    likes_number = models.IntegerField(
        verbose_name="Количество лайков",
        default=0
    )
    city = models.ForeignKey(
        to=City,
        on_delete=models.RESTRICT,
        related_name="profile_photos",
        verbose_name="Город, где сделано фото"
    )
    is_title = models.BooleanField(
        default=False,
        verbose_name="Аватарка"
    )
