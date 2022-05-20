from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class Phone(AbstractDateTime):  # noqa
    phone = models.CharField(
        max_length=12,
        verbose_name="Номер телефона"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        related_name="phones",
        verbose_name="Владелец"
    )


class Chat(AbstractDateTime):  # noqa
    is_group = models.BooleanField(
        verbose_name="Группа",
        default=False
    )
    photo = models.ImageField(
        upload_to='photos/chats/%Y/%m/%d/',
        blank=True,
        verbose_name='Миниатюра'
    )
    members = models.ManyToManyField(
        through="ChatMember",
        through_fields=("user", "chat"),
        related_name="joined_chats",
        blank=True,
        verbose_name="Члены чата"
    )
    class Meta:  # noqa
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ["-datetime_updated"]


class ChatMember(models.Model):  # noqa
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="chats",
        verbose_name="Пользователь"
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.RESTRICT,
        related_name="members",
        verbose_name="Чат"
    )
    chat_name = models.CharField(
        max_length=150,
        default=user.username,
        verbose_name="Никнейм в чате"
    )


class Message(AbstractDateTime):  # noqa
    content = models.TextField(
        verbose_name="Конент"
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.RESTRICT,
        related_name="messages",
        verbose_name="Чат"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="messages",
        verbose_name="Владелец"
    )

    class Meta:  # noqa
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-datetime_created"]


class Privilege(AbstractDateTime):  # noqa
    MAX_PRIVILEGE_NAME = 50
    name = models.CharField(
        verbose_name="Наименование",
        unique=True,
        max_length=MAX_PRIVILEGE_NAME
    )


class Position(AbstractDateTime):  # noqa
    MAX_POSITION_NAME = 50
    name = models.CharField(
        verbose_name="Наименование",
        unique=True,
        max_length=MAX_POSITION_NAME
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )
    privileges = models.ManyToManyField(
        to=Privilege,
        related_name="positions"
    )


class ComplainReason(AbstractDateTime):  # noqa
    MAX_COMPLAIN_NAME = 100
    name = models.CharField(
        max_length=MAX_COMPLAIN_NAME,
        unique=True,
        verbose_name="Наименование"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


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


class Group(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=100,
        verbose_name="Название группы"
    )
    followers = models.ManyToManyField(
        to=CustomUser,
        related_name="groups",
        blank=True,
        verbose_name="Подписчики"
    )
    members_rights = models.ManyToManyField(
        to=CustomUser,
        through="GroupAdministration",
        through_fields=("user", "group"),
        related_name="group_rights",
        verbose_name="Позиция в группе"
    )


class GroupAdministration(AbstractDateTime):  # noqa
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        verbose_name="Пользователь группы"
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.RESTRICT,
        verbose_name="Группа"
    )
    position = models.ForeignKey(
        to=Position,
        on_delete=models.RESTRICT,
        verbose_name="Статус"
    )


class Performer(AbstractDateTime):  # noqa
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Никнейм"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Фамилия"
    )


class Playlist(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=150,
        verbose_name="Название плэйлиста"
    )
    photo = models.ImageField(
        uploaded_to="photos/playlists/%Y/%m/%d",
        blank=True,
        verbose_name="Фото плэйлиста"
    )
    listeners = models.ManyToManyField(
        to=CustomUser,
        related_name="playlists",
        verbose_name="Слушатели",
        blank=True
    )


class Music(AbstractDateTime):  # noqa
    music = models.FileField(
        upload_to="documents/songs/%Y/%m/%d",
        verbose_name="Файл песни",
        unique=True
    )
    playlist = models.ForeignKey(
        to=Playlist,
        on_delete=models.RESTRICT,
        related_name="playlist_songs",
        verbose_name="Плэйлист"
    )
    performers = models.ManyToManyField(
        to=Performer,
        related_name="performer_songs",
        verbose_name="Певцы"
    )
    users = models.ManyToManyField(
        to=CustomUser,
        related_name="user_songs",
        verbose_name="Пользователи",
        blank=True
    )


class Video(AbstractDateTime):  # noqa

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


class Country(AbstractDateTime):  # noqa
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название страны"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Url"
    )


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


class ProfilePhoto(AbstractDateTime):  # noqa
    photo = models.ImageField(
        upload_to="photos/profile_photos/%Y/%m/%d",
        verbose_name="Фото профиля"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="profile_photos"
    )
    likes_number = models.IntegerField(
        verbose_name="Количество лайков",
        default=0
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
