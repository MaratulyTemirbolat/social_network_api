from datetime import datetime

from django.db import models


class AbstractDateTime(models.Model):  # noqa
    datetime_created = models.DateTimeField(
        verbose_name='время создания',
        auto_now_add=True
    )
    datetime_updated = models.DateTimeField(
        verbose_name='время обновления',
        auto_now=True
    )
    datetime_deleted = models.DateTimeField(
        verbose_name='время удаления',
        null=True,
        blank=True
    )

    class Meta:  # noqa
        abstract = True

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        super().save(*args, **kwargs)

    def delete(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        datetime_now: datetime = datetime.now()
        self.datetime_deleted = datetime_now
        self.save(
            update_fields=['datetime_deleted']
        )
