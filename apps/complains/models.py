from django.db import models
from django.utils.text import slugify

from abstracts.models import AbstractDateTime
from auths.models import CustomUser
from news.models import News


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


class ComplainNews(AbstractDateTime):  # noqa
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
    news = models.ForeignKey(
        to=News,
        on_delete=models.RESTRICT,
        related_name="n_complains",
        verbose_name="Новость"
    )

    class Meta:  # noqa
        verbose_name = "Жалоба новости"
        verbose_name_plural = "Жалобы новостей"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'{self.owner} пожаловался на новость по причине {self.reason}'
