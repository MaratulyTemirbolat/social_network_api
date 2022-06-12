from typing import (
    Any,
    Tuple,
    List,
    Optional,
)

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet


class ProfilePhotoCityFilter(SimpleListFilter):  # noqa
    title: str = "Геопозиция фоток"
    parameter_name: str = "decade"

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:  # noqa
        return [
            ('with_city', "С геопозицией города"),
            ('without_city', "Без геопозиции города"),
        ]

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:  # noqa
        if self.value() == 'with_city':
            return queryset.get_photo_with_city()
        if self.value() == 'without_city':
            return queryset.get_photo_without_city()
