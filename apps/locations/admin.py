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
    City,
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


@admin.register(City)
class CityModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_updated",
        "datetime_created",
    )
    search_fields: Tuple[str] = (
        "id", "name",
    )
    list_display: Tuple[str] = (
        "id", "name", "country", "is_capital",
        "get_is_deleted",
    )
    list_filter: Tuple[Any, str] = (
        CommonStateFilter,
        "is_capital",
    )
    list_display_links: Tuple[str] = (
        "id", "name",
    )
    list_editable: Tuple[str] = (
        "country",
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[City] = None
    ) -> tuple:  # noqa
        if not obj:
            return self.readonly_fields
        return self.readonly_fields + (
            'country',
        )

    def get_is_deleted(self, obj: Optional[City] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Город удален</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Город не удален</p>'
            )
    get_is_deleted.short_description = "Существование города"
    get_is_deleted.empty_value_display = "Город не удален"
