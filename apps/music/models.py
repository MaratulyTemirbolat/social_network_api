from django.db import models
from django.utils.text import slugify

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class Playlist(AbstractDateTime):  # noqa
    PLAYLIST_MAX_NAME_LEN = 150
    name = models.CharField(
        max_length=PLAYLIST_MAX_NAME_LEN,
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

    class Meta:  # noqa
        verbose_name = "Плэйлист"
        verbose_name_plural = "Плэйлисты"
        ordering = (
            "datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f"Плэйлист \"{self.name}\""


class Performer(AbstractDateTime):  # noqa
    PERFORMER_MAX_USERNAME_LEN = 100
    PERFORMER_MAX_NAME_SURNAME_LEN = 100
    username = models.CharField(
        max_length=PERFORMER_MAX_USERNAME_LEN,
        unique=True,
        verbose_name="Никнейм"
    )
    slug = models.SlugField(
        max_length=PERFORMER_MAX_USERNAME_LEN,
        unique=True,
        help_text="URL для поиска на основе никнейма исполнителя",
        verbose_name="Url"
    )
    name = models.CharField(
        max_length=PERFORMER_MAX_NAME_SURNAME_LEN,
        verbose_name="Имя"
    )
    surname = models.CharField(
        max_length=PERFORMER_MAX_NAME_SURNAME_LEN,
        verbose_name="Фамилия"
    )

    class Meta:  # noqa
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"
        ordering = (
            "datetime_updated",
        )

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f"Исполнитель \"{self.username}\""


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

    class Meta:  # noqa
        verbose_name = "Музыка"
        verbose_name_plural = "Музыки"
        ordering = (
            "datetime_updated",
        )
