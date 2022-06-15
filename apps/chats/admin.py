from typing import (
    Dict,
    Any,
    Optional,
    Sequence,
    Tuple,
)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.handlers.wsgi import WSGIRequest

from chats.models import (
    Chat,
    ChatMember,
    Message,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):  # noqa
    fields: Tuple[str] = (
        ("name", "slug",),
        "is_group", "photo",
    )
    readonly_fields: Sequence[str] = (
        "datetime_created",
        "datetime_updated",
        "datetime_deleted",
    )
    list_display: Tuple[str] = (
        "id", "name", "slug",
        "get_photo", "get_is_deleted",
    )
    search_fields: Sequence[str] = (
        "name", "slug",
    )
    list_filter: Tuple[str, Any] = (
        "is_group",
        CommonStateFilter
    )
    list_display_links: Tuple[str] = (
        "id", "name", "slug",
    )
    list_per_page: int = 10
    save_on_top: bool = True

    def get_photo(self, obj: Optional[Chat] = None) -> str:  # noqa
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" height="100">')
    get_photo.short_description = "Фото чата"
    get_photo.empty_value_display = "No photo uploaded"

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Chat] = None
    ) -> tuple:  # noqa
        if not obj:
            return self.readonly_fields
        return self.readonly_fields + (
            'slug',
        )

    def get_is_deleted(self, obj: Optional[Chat] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Чат удалён</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Чат не удален</p>'
            )
    get_is_deleted.short_description = "Существование чата"
    get_is_deleted.empty_value_display = "Чат не удален"


@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):  # noqa
    list_display: Tuple[str] = (
        "id", "chat", "user", "chat_name",
    )
    list_per_page: int = 25
    list_display_links: Tuple[str] = (
        "id", "chat", "user",
    )
    search_fields: Sequence[str] = (
        "chat_name",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Sequence[str] = (
        "datetime_created",
        "datetime_deleted",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "id", "chat", "owner",
        "get_shorted_content",
        "get_is_deleted",
    )
    search_fields: Sequence[str] = (
        "id", "content",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    list_display_links: Tuple[str] = (
        "id", "owner", "chat",
    )
    list_per_page: int = 20

    def get_is_deleted(self, obj: Optional[Message] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Сообщение удалено</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Сообщение не удалено</p>'
            )
    get_is_deleted.short_description = "Существование сообщения"
    get_is_deleted.empty_value_display = "Сообщение не удалено"

    def get_shorted_content(self, obj: Message):
        """Get short version of content."""
        if obj.content:
            return f"{obj.content[:25]}..."
    get_shorted_content.short_description = "Контент сообщения"
