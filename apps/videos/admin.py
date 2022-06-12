from typing import (
    Tuple,
    Any,
    Optional,
    Dict,
)

from django.contrib import admin
from django.utils.safestring import mark_safe

from videos.models import (
    Video,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(Video)
class VideoModel(admin.ModelAdmin):  # noqa
    fieldsets: Tuple[Tuple[str, Dict[str, Tuple[str]]]] = (
        ('Инормация о видео', {
            'fields': (
                'name',
                'video_file',
                'owner',
            )
        }),
        ('Люди, которые добавили видео', {
            'fields': (
                'keepers',
            )
        }),
        ('История новости', {
            'fields': (
                'datetime_created',
                'datetime_deleted',
                'datetime_updated',
            )
        })
    )
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_updated",
        "datetime_created",
    )
    filter_horizontal: Tuple[str] = (
        "keepers",
    )
    list_display: Tuple[str] = (
        "id", "name", "owner",
        "get_is_deleted",
    )
    search_fields: Tuple[str] = (
        "name",
    )
    list_display_links: Tuple[str] = (
        "id", "name",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    save_on_top: bool = True

    def get_is_deleted(self, obj: Optional[Video] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Видео удалено</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Видео не удалено</p>'
            )
    get_is_deleted.short_description = "Существование видео"
    get_is_deleted.empty_value_display = "Видео не удалено"
