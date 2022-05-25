from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class Playlist(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=150,
        verbose_name="Название плэйлиста"
    )
    photo = models.ImageField(
        upload_to="photos/playlists/%Y/%m/%d",
        blank=True,
        verbose_name="Фото плэйлиста"
    )
    listeners = models.ManyToManyField(
        to=CustomUser,
        related_name="playlists",
        verbose_name="Слушатели",
        blank=True
    )


class Performer(AbstractDateTime):  # noqa
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Никнейм"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Фамилия"
    )


class Music(AbstractDateTime):  # noqa
    music = models.FileField(
        upload_to="documents/songs/%Y/%m/%d",
        verbose_name="Файл песни",
        unique=True
    )
    playlist = models.ForeignKey(
        to=Playlist,
        on_delete=models.RESTRICT,
        related_name="playlist_songs",
        verbose_name="Плэйлист"
    )
    performers = models.ManyToManyField(
        to=Performer,
        related_name="performer_songs",
        verbose_name="Певцы"
    )
    users = models.ManyToManyField(
        to=CustomUser,
        related_name="user_songs",
        verbose_name="Пользователи",
        blank=True
    )
