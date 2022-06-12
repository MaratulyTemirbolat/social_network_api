from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser
from locations.models import City


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
