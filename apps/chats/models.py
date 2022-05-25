from django.db import models

from abstracts.models import AbstractDateTime
from auths.models import CustomUser


class Chat(AbstractDateTime):  # noqa
    CHAT_MAX_NAME_LENGTH = 150
    URL_MAX_LENGTH = 50
    name = models.CharField(
        max_length=CHAT_MAX_NAME_LENGTH,
        verbose_name="Название чата"
    )
    slug = models.SlugField(
        max_length=URL_MAX_LENGTH,
        unique=True,
        verbose_name="URL (ссылка на чат)",
        help_text="URL для поиска чата"
    )
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
        to=CustomUser,
        through="ChatMember",
        through_fields=("chat", "user"),
        related_name="joined_chats",
        blank=True,
        verbose_name="Члены чата"
    )
    class Meta:  # noqa
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = (
            "-datetime_updated",
        )


class ChatMember(models.Model):  # noqa
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.RESTRICT,
        verbose_name="Чат"
    )
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        verbose_name="Пользователь"
    )
    chat_name = models.CharField(
        max_length=150,
        default=None,
        null=True,
        blank=True,
        verbose_name="Никнейм в чате"
    )

    class Meta:  # noqa
        verbose_name = "Член чата"
        verbose_name_plural = "Члены чата"
        ordering = (
            "id",
        )
        constraints = [
            models.UniqueConstraint(
                fields=['chat', 'user'],
                name="unique_chat_user"
            ),
        ]

    def __str__(self) -> str:  # noqa
        return f'Пользователь {self.user} в чате \
{self.chat} с никнеймом {self.chat_name}'


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
        ordering = (
            "-datetime_created",
        )

    def __str__(self) -> str:  # noqa
        return f'Сообщение создал пользователь {self.owner} в чате {self.chat}'
