from django.db import models
from django.utils.text import slugify

from abstracts.models import AbstractDateTime
from auths.models import CustomUser
from groups.models import Group


class Tag(AbstractDateTime):  # noqa
    TAG_MAX_NAME_LEN = 100
    name = models.CharField(
        max_length=TAG_MAX_NAME_LEN,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=TAG_MAX_NAME_LEN,
        unique=True,
        blank=True,
        verbose_name="Url",
        help_text="URL для поиска тэга по его наименованию"
    )

    class Meta:  # noqa
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f"Тэг \"{self.name}\""

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(AbstractDateTime):  # noqa
    CATEGORY_TITLE_MAX_LEN = 100
    title = models.CharField(
        max_length=CATEGORY_TITLE_MAX_LEN,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=CATEGORY_TITLE_MAX_LEN,
        unique=True,
        verbose_name="Url",
        help_text="URL для поиска категории по его наименованию"
    )

    class Meta:  # noqa
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = (
            "-datetime_updated",
        )

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f'Категория {self.title}'


class News(AbstractDateTime):  # noqa
    photo = models.ImageField(
        upload_to="photos/news/%Y/%m/%d",
        verbose_name="Миниатюра"
    )
    content = models.TextField(
        verbose_name="Контент новости"
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name="group_news",
        verbose_name="Создано группой"
    )
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name="published_news",
        verbose_name="Автор новости"
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.RESTRICT,
        related_name="news",
        verbose_name="Категория"
    )
    liked_users = models.ManyToManyField(
        to=CustomUser,
        related_name="liked_posts",
        verbose_name="Лайки ползователей",
        blank=True
    )
    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        related_name="news",
        verbose_name="Тэги"
    )

    class Meta:  # noqa
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = (
            "datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'Новость {self.content[:50]}'


class Comment(AbstractDateTime):  # noqa
    content = models.TextField(
        verbose_name="Контент"
    )
    likes = models.ManyToManyField(
        to=CustomUser,
        related_name="liked_comments",
        blank=True,
        verbose_name="Лайки пользователей"
    )
    commentator = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="comments",
        verbose_name="Владелец комментария"
    )
    news = models.ForeignKey(
        to=News,
        on_delete=models.RESTRICT,
        related_name="comments",
        verbose_name="Новость"
    )

    class Meta:  # noqa
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = (
            "-datetime_updated",
        )

    def __str__(self) -> str:  # noqa
        return f'Пользователь {self.commentator} прокомментировал {self.news}'