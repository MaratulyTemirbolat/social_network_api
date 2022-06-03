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
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'name',
                'slug',
                'is_group',
                'photo',
            ),
        }),
    )
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
        "name", "slug",
        "get_photo",
    )
    search_fields: Sequence[str] = (
        "name", "slug",
    )
    list_filter: Tuple[str, Any] = (
        "is_group",
        CommonStateFilter
    )
    save_on_top: bool = True

    def get_photo(self, obj: Optional[Chat]) -> str:  # noqa
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


@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):  # noqa
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Sequence[str] = (
        "datetime_created",
        "datetime_deleted",
        "datetime_updated",
    )
