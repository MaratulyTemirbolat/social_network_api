from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import (
    CustomUser,
)

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
