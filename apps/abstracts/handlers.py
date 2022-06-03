from typing import (
    Optional,
)


from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.pagination import BasePagination
from rest_framework.serializers import Serializer

from django.db.models import QuerySet


class DRFResponseHandler:
    """Handler for DRF response."""

    def get_drf_response(
        self,
        request: DRF_Request,
        data: QuerySet,
        serializer_class: Serializer,
        many: bool = False,
        paginator: Optional[BasePagination] = None
    ) -> DRF_Response:  # noqa
        if paginator:
            objects: list = paginator.paginate_queryset(
                data,
                request
            )
            serializer: Serializer = serializer_class(
                objects,
                many=many
            )
            response: DRF_Response = \
                paginator.get_paginated_response(
                    serializer.data
                )
            return response

        serializer: Serializer = serializer_class(
            data,
            many=many
        )
        response: DRF_Response = DRF_Response(
            {
                'data': serializer.data
            }
        )
        return response
