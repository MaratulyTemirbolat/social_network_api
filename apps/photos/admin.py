from typing import (
    Tuple,
    Optional,
    Any,
)

from django.contrib import admin
from django.utils.safestring import mark_safe

from photos.models import (
    ProfilePhoto,
)
from abstracts.filters import CommonStateFilter
from photos.filters import ProfilePhotoCityFilter


@admin.register(ProfilePhoto)
class ProfilePhotoModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
        "likes_number",
    )
    list_display: Tuple[str] = (
        "id", "get_photo",
        "owner", "likes_number",
        "city", "is_title",
        "get_is_deleted",
    )
    list_display_links: Tuple[str] = (
        "id", "owner", "get_photo",
    )
    list_filter: Tuple[Any, str] = (
        CommonStateFilter,
        'is_title',
        ProfilePhotoCityFilter,
    )
    search_fields: Tuple[str] = (
        "description",
    )
    list_per_page: int = 10

    def get_photo(self, obj: Optional[ProfilePhoto] = None) -> str:  # noqa
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" height="100">')
    get_photo.short_description = "Фото в профиле"
    get_photo.empty_value_display = "No photo uploaded"

    def get_is_deleted(self, obj: Optional[ProfilePhoto] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Фотография удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Фотография не удалена</p>'
            )
    get_is_deleted.short_description = "Существование фотографии"
    get_is_deleted.empty_value_display = "Фотография не удалена"
