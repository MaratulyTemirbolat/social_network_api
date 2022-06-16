from typing import (
    Any,
    Tuple,
)

from django.db.models import QuerySet

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.permissions import IsAdminUser

from chats.models import Chat
from chats.serializers import ChatModelSerializer
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator


class ChatViewSet(DRFResponseHandler, ViewSet):
    """Chat class ViewSet."""

    queryset: QuerySet[Chat] = \
        Chat.objects.all()
    serializer_class: ChatModelSerializer = ChatModelSerializer
    permission_classes: Tuple[Any] = (
        IsAdminUser,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self):
        """Queryset method for ORM."""
        return self.queryset.get_not_deleted().prefetch_related("members")

    def list(self, request: DRF_Request) -> DRF_Response:
        """List method for GET-request."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class(),
            serializer_context={"request": request}
        )
        return response
