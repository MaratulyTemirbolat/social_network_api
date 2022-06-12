from typing import (
    Tuple,
    Dict,
    Optional,
    Any,
)

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe

from locations.models import (
    Country,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(Country)
class CountryModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
        "slug",
    )
    list_display: Tuple[str] = (
        "id", "name", "slug",
        "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    search_fields: Tuple[str] = (
        "id", "name", "slug",
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Country] = None
    ) -> tuple:  # noqa
        if not obj:
            return self.readonly_fields
        return self.readonly_fields + (
            'name',
        )

    def get_is_deleted(self, obj: Optional[Country] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Страна удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Страна не удалена</p>'
            )
    get_is_deleted.short_description = "Существование страны"
    get_is_deleted.empty_value_display = "Страна не удалена"
