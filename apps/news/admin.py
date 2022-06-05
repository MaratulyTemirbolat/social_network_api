from atexit import register
from typing import (
    Tuple,
    Any,
    Optional,
)

from django.contrib import admin
from django.utils.safestring import mark_safe

from news.models import (
    Tag,
    Category,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
        "slug",
    )
    list_display: Tuple[str] = (
        "name", "slug",
        "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    search_fields: Tuple[str] = (
        "name",
        "slug",
    )

    def get_is_deleted(self, obj: Optional[Tag] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Тэг удален</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Тэг не удален</p>'
            )
    get_is_deleted.short_description = "Существование тэга"
    get_is_deleted.empty_value_display = "Тэг не удален"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "slug",
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "id",
        "title",
        "slug",
        "get_is_deleted",
    )
    search_fields: Tuple[str] = (
        "title",
        "slug",
    )
    list_display_links: Tuple[str] = (
        "title",
        "slug",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )

    def get_is_deleted(self, obj: Optional[Category] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Категория удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Категория не удалена</p>'
            )
    get_is_deleted.short_description = "Существование категории"
    get_is_deleted.empty_value_display = "Категория не удалена"
