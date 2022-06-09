from tabnanny import verbose
from django.db import models
from django.utils.text import slugify

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class ComplainReason(AbstractDateTime):  # noqa
    MAX_COMPLAIN_NAME_LEN = 100
    name = models.CharField(
        max_length=MAX_COMPLAIN_NAME_LEN,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=MAX_COMPLAIN_NAME_LEN,
        unique=True,
        verbose_name="Url",
        help_text="URL для поиска причина жалобы по её наименованию"
    )

    class Meta:  # noqa
        verbose_name = "Причина жалобы"
        verbose_name_plural = "Причины жалоб"
        ordering = (
            "-datetime_updated",
        )

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f"Причина: \"{self.name}\""


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

    class Meta:  # noqa
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'{self.owner} пожаловался по причине {self.reason}'


class Video(AbstractDateTime):  # noqa
    VIDEO_NAME_MAX_LEN = 250
    name = models.CharField(
        max_length=VIDEO_NAME_MAX_LEN,
        verbose_name="Название видео"
    )
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

    class Meta: # noqa
        verbose_name = "Видео"
        verbose_name_plural = "Видосики"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'Видео {self.name}. Владелец {self.owner}'


class Country(AbstractDateTime):  # noqa
    COUNTRY_NAME_MAX_LEN = 100
    name = models.CharField(
        max_length=COUNTRY_NAME_MAX_LEN,
        unique=True,
        verbose_name="Название страны"
    )
    slug = models.SlugField(
        max_length=COUNTRY_NAME_MAX_LEN,
        unique=True,
        verbose_name="Url",
        help_text="URL для поиска страны по её названию"
    )

    class Meta:  # noqa
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = (
            "-datetime_updated",
        )

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f"Страна {self.name}"


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
    is_capital = models.BooleanField(
        default=False,
        verbose_name="Столица"
    )

    class Meta:  # noqa
        verbose_name = "Город"
        verbose_name_plural = "Столицы"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        if self.is_capital:
            return f'Столица {self.country}, город {self.name}'
        return f'Город {self.name} в {self.country}'


class ProfilePhoto(AbstractDateTime):  # noqa
    photo = models.ImageField(
        upload_to="photos/profile_photos/%Y/%m/%d",
        verbose_name="Фото профиля"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="profile_photos",
        verbose_name="Владелец"
    )
    likes_number = models.IntegerField(
        default=0,
        verbose_name="Количество лайков"
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

    class Meta:  # noqa
        verbose_name = "Фотография профиля"
        verbose_name_plural = "Фотографии профиля"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        if self.is_title:
            return f"Главная аватарка пользователя {self.owner}"
        return f"Одна из фотографий пользователя {self.owner}"
