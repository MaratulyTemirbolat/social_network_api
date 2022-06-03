from typing import (
    Any,
    Tuple,
    List,
    Optional,
)

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet


class CommonStateFilter(SimpleListFilter):  # noqa
    title: str = "Состояние"
    parameter_name: str = "pages"

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:  # noqa
        # breakpoint()
        return [
            ('deleted', "Удаленные"),
            ('not_deleted', "Неудаленные"),
        ]

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:  # noqa
        # breakpoint()
        if self.value() == 'deleted':
            return queryset.get_deleted()
        if self.value() == 'not_deleted':
            return queryset.get_not_deleted()
