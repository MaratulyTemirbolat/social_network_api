from typing import (
    Any,
    Optional,
    Tuple,
    Dict,
    List,
)

from django.db.models import QuerySet

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from abstracts.mixins import (
    DeletedRequestMixin,
    ModelInstanceMixin,
)
from abstracts.paginators import AbstractPageNumberPaginator
from abstracts.handlers import NoneDataHandler
from abstracts.models import AbstractDateTimeQuerySet
from videos.models import Video
from videos.serializers import VideoBaseModelSerializer


class VideoViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """VideoViewSet."""

    queryset: QuerySet[Video] = \
        Video.objects.all()
    serializer_class: VideoBaseModelSerializer = VideoBaseModelSerializer
    permission_classes: Tuple[Any] = (
        IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request for all videos."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )

        return response
