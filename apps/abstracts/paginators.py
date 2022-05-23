"""Abstract custom paginators."""
from rest_framework.response import Response as DRF_Response
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)
from rest_framework.utils.serializer_helpers import ReturnList


class AbstractPageNumberPaginator(PageNumberPagination):
    """AbstractPageNumberPaginator."""

    page_size: int = 2
    page_size_query_param: str = 'page_size'
    page_query_param: str = 'page'
    max_page_size: int = 10

    def get_paginated_response(self, data: ReturnList) -> DRF_Response:
        """Overriden method."""
        response: DRF_Response = DRF_Response(
            {
                'pagination': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'count': self.page.paginator.num_pages,
                },
                'data': data
            }
        )
        return response


class AbstractLimitOffsetPaginator(LimitOffsetPagination):
    """AbstractLimitOffsetPaginator."""

    limit: int = 2
    limit_query_param: str = 'limit'
    offset: int = 0
    offset_query_param: str = 'offset'
    max_limit: int = 5

    def get_paginated_response(self, data: ReturnList) -> DRF_Response:
        """Overriden method."""
        response: DRF_Response = \
            DRF_Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link(),
                    },
                    'data': data
                }
            )
        return response
