from typing import (
    Sequence,
    Tuple,
    Any,
    Optional,
)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.handlers.wsgi import WSGIRequest

from music.models import (
    Playlist,
    Performer,
    Music,
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
    list_per_page: int = 10

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


@admin.register(Performer)
class PerformerModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_created",
        "datetime_deleted",
        "datetime_updated",
        "slug",
    )
    fieldsets: Tuple = (
        ('Информация об исполнителе (в сети)', {
            'fields': (
                ('username', 'slug',),
            )
        }),
        ('Личная информация об исполнителе', {
            'fields': (
                ('name', 'surname',),
            )
        }),
        ('История', {
            'fields': (
                'datetime_deleted',
                'datetime_created',
                'datetime_updated',
            )
        })
    )
    list_display: Tuple[str] = (
        "username",
        "slug",
        "name",
        "surname",
        "get_is_deleted",
    )
    search_fields: Tuple[str] = (
        "username",
        "slug",
        "name",
        "surname",
    )
    list_filter: Tuple[str] = (
        CommonStateFilter,
    )
    list_display_links: Tuple[str] = (
        "username",
        "slug",
    )
    list_editable: Sequence[str] = (
        "name",
        "surname",
    )
    list_per_page: int = 10

    def get_is_deleted(self, obj: Optional[Playlist] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Исполнитель удалён</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Исполнитель не удалён</p>'
            )
    get_is_deleted.short_description = "Существование исполнителя"
    get_is_deleted.empty_value_display = "Исполнитель не удалён"


@admin.register(Music)
class MusicModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    filter_horizontal: Tuple[str] = (
        "performers",
        "users",
    )
    fieldsets: Tuple = (
        ('Информация о музыке', {
            'fields': (
                'music',
                'playlist',
            )
        }),
        ('Исполнители и слушатели', {
            'fields': (
                'performers',
                'users',
            )
        }),
        ('История музыки', {
            'fields': (
                'datetime_deleted',
                'datetime_created',
                'datetime_updated',
            )
        })
    )
    list_display: Tuple[str] = (
        "id", "music",
        "playlist", "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
        "performers",
    )
    list_display_links: Tuple[str] = (
        "id", "playlist",
    )

    def get_is_deleted(self, obj: Optional[Playlist] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Музыка удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Музыка не удалена</p>'
            )
    get_is_deleted.short_description = "Существование музыки"
    get_is_deleted.empty_value_display = "Музыка не удалена"

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Music] = None
    ) -> Sequence[str]:  # noqa
        if obj:
            return self.readonly_fields + ("performers",)
        return self.readonly_fields
