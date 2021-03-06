from typing import (
    Tuple,
    Any,
    Dict,
    Optional,
)

from django.contrib import admin
from django.utils.safestring import mark_safe

from complains.models import (
    ComplainReason,
    ComplainNews,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(ComplainReason)
class ComplainReasonModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "id",
        "name",
        "slug",
        "get_is_deleted",
    )
    prepopulated_fields: Dict[str, Tuple[str]] = {
        "slug": ("name",),
    }
    search_fields: Tuple[str] = (
        "name", "slug",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )

    def get_is_deleted(self, obj: Optional[ComplainReason] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Причина жалобы удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Причина жалобы не удалена</p>'
            )
    get_is_deleted.short_description = "Существование причины"
    get_is_deleted.empty_value_display = "Причина жалобы не удалена"


@admin.register(ComplainNews)
class ComplainNewsModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "id",
        "owner",
        "reason",
        "news",
    )
    save_on_top: bool = True
    search_fields: Tuple[str] = (
        "content",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )

    def get_is_deleted(self, obj: Optional[ComplainNews] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Жалоба удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Жалоба не удалена</p>'
            )
    get_is_deleted.short_description = "Существование жалобы"
    get_is_deleted.empty_value_display = "Жалоба не удалена"
