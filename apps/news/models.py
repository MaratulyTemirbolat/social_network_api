from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser
from groups.models import Group


class Tag(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


class Category(AbstractDateTime):  # noqa
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


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
