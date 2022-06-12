from django.db import models
from django.utils.text import slugify

from abstracts.models import AbstractDateTime


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
