from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import (
    CustomUser,
)
from videos.validators import video_format_validator


class Video(AbstractDateTime):  # noqa
    VIDEO_NAME_MAX_LEN = 250
    name = models.CharField(
        max_length=VIDEO_NAME_MAX_LEN,
        verbose_name="Название видео"
    )
    video_file = models.FileField(
        upload_to="documents/videos/%Y/%m/%d",
        verbose_name="Видео файл",
        validators=[video_format_validator]
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="owned_videos",
        verbose_name="Владелец"
    )
    keepers = models.ManyToManyField(
        to=CustomUser,
        through="VideoKeeper",
        through_fields=("video", "user"),
        blank=True,
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


class VideoKeeper(models.Model):
    """VideoKeeper."""

    video = models.ForeignKey(
        to=Video,
        on_delete=models.CASCADE,
        verbose_name="Видео"
    )
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    class Meta:
        """Customization of the Table."""

        verbose_name = "Добавленное видео"
        verbose_name_plural = "Добавленные видео"
        ordering = (
            "id",
        )
        constraints = [
            models.UniqueConstraint(
                fields=['video', 'user'],
                name="unique_video_user"
            ),
        ]
        index_together = [
            ("video", "user"),
        ]

    def __str__(self) -> str:
        """Override methode str."""
        return f"{self.user} {self.video}"
