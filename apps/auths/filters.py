from typing import (
    Any,
    Tuple,
    List,
    Optional,
)

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest


class CommonStateFilter(SimpleListFilter):  # noqa
    title: str = "Состояние"
    parameter_name: str = "pages"

    def lookups(
        self,
        request: WSGIRequest,
        model_admin: Any
    ) -> List[Tuple[Any, str]]:  # noqa
        return [
            ('deleted', "Удаленные"),
            ('not_deleted', "Неудаленные"),
        ]

    def queryset(
        self,
        request: WSGIRequest,
        queryset: QuerySet
    ) -> Optional[QuerySet]:  # noqa
        if self.value() == 'deleted':
            return queryset.filter(datetime_deleted__isnull=False)
        if self.value() == 'not_deleted':
            return queryset.filter(datetime_deleted__isnull=True)
