from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="owned_chats",
        verbose_name="Создатель чата"
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

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        if self.slug:
            self.slug = slugify(self.slug)
        # breakpoint()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f"Чат \"{self.name}\""


class ChatMemberQuerySet(QuerySet):  # noqa
    def get_number_of_members(self, chat_id: int) -> int:  # noqa
        return self.filter(
            chat_id=chat_id
        ).count()


class ChatMember(models.Model):  # noqa
    CHAT_USER_NAME_MAX_LEN = 150
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
        max_length=CHAT_USER_NAME_MAX_LEN,
        default=None,
        null=True,
        blank=True,
        verbose_name="Никнейм в чате"
    )
    objects = ChatMemberQuerySet.as_manager()

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

    def __get_number_of_members(self) -> int:
        return ChatMember.objects.filter(
            chat_id=self.chat_id
        ).count()

    def is_amount_members_sufficient(self) -> None:  # noqa
        TWO_MEMBERS = 2
        if not self.chat.is_group:
            chats_members: int = self.__get_number_of_members()
            if chats_members >= TWO_MEMBERS:
                raise ValidationError(
                    message="Нелья добавлять еще людей не в групповой чат",
                    code="max_chat_members"
                )

    def clean(self) -> None:  # noqa
        self.is_amount_members_sufficient()
        return super().clean()

    def save(
        self,
        *args: tuple,
        **kwargs: dict
    ) -> None:  # noqa
        if not self.chat_name:
            self.chat_name = self.user.username
        return super().save(*args, **kwargs)

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
