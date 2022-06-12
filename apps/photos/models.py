from datetime import datetime

from django.db import models
from django.db.models import QuerySet

from abstracts.models import (
    AbstractDateTime,
    AbstractDateTimeQuerySet,
)
from auths.models import CustomUser
from locations.models import City


class ProfilePhotoQuerySet(AbstractDateTimeQuerySet):  # noqa
    def get_photo_with_city(self) -> QuerySet:  # noqa
        return self.filter(
            city__isnull=False
        )

    def get_photo_without_city(self) -> QuerySet:  # noqa
        return self.filter(
            city__isnull=True
        )


class ProfilePhoto(AbstractDateTime):  # noqa
    photo = models.ImageField(
        upload_to="photos/profile_photos/%Y/%m/%d",
        verbose_name="Фото профиля"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание фото"
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
        blank=True,
        null=True,
        related_name="profile_photos",
        verbose_name="Город, где сделано фото"
    )
    is_title = models.BooleanField(
        default=False,
        verbose_name="Аватарка"
    )
    objects = ProfilePhotoQuerySet.as_manager()

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

    def __change_title_photo(self) -> None:  # noqa
        is_prev_title_exist: bool = ProfilePhoto.objects.filter(
            owner=self.owner,
            is_title=True
        ).exists()
        if is_prev_title_exist and self.is_title:
            prev_photo: ProfilePhoto = ProfilePhoto.objects.get(
                owner=self.owner,
                is_title=True
            )
            prev_photo.is_title = False
            prev_photo.save(
                update_fields=['is_title']
            )
        elif not is_prev_title_exist:
            self.is_title = True

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.__change_title_photo()
        return super().save(*args, **kwargs)

    def delete(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        datetime_now: datetime = datetime.now()
        self.datetime_deleted = datetime_now
        self.is_title = False
        self.save(
            update_fields=['datetime_deleted', 'is_title']
        )
