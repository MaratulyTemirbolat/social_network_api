from typing import (
    Sequence,
    Tuple,
    Any,
    Optional,
)

from django.contrib import admin
from django.utils.safestring import mark_safe

from music.models import (
    Playlist,
)
from abstracts.filters import CommonStateFilter


@admin.register(Playlist)
class PlaylistModel(admin.ModelAdmin):  # noqa
    fieldsets: Tuple = (
        ('Информация о плэйлисте', {
            'fields': (
                'name',
                'photo',
            )
        }),
        ('Слушатели', {
            'fields': (
                'listeners',
            )
        }),
        ('История плэйлиста', {
            'fields': (
                'datetime_deleted',
                'datetime_created',
                'datetime_updated',
            )
        })
    )
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "name",
        "get_photo",
        "get_is_deleted",
    )
    filter_horizontal: Sequence[str] = (
        "listeners",
    )
    search_fields: Sequence[str] = (
        "name",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )

    def get_photo(self, obj: Optional[Playlist] = None) -> str:  # noqa
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" height="100">')
    get_photo.short_description = "Фото плэйлиста"
    get_photo.empty_value_display = "Фото не загружено"

    def get_is_deleted(self, obj: Optional[Playlist] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:20px;">\
Плэйлист удалён</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:20px;">\
Плэйлист не удалён</p>'
            )
    get_is_deleted.short_description = "Существование плэйлиста"
    get_is_deleted.empty_value_display = "Плэйлист не удалён"
