from typing import (
    Any,
    Optional,
    Tuple,
    Dict,
)

from django.db.models import (
    QuerySet,
)
from django.utils.text import slugify
from django.http.request import QueryDict

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from chats.models import (
    Chat,
)
from chats.serializers import (
    ChatCreateSerializer,
    ChatViewSerializer,
)
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator


class ChatModelApiView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatViewSerializer
    pagination_class = AbstractPageNumberPaginator
    permission_classes = ()

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ):  # noqa
        self.serializer_class = ChatCreateSerializer
        my_data = request.data.copy()
        my_data["slug"] = slugify(my_data["slug"])
        serializer = self.get_serializer(data=my_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return DRF_Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )



class ChatViewSet(DRFResponseHandler, ViewSet):
    """Chat class ViewSet."""

    queryset: QuerySet[Chat] = \
        Chat.objects.all()
    serializer_class: ChatViewSerializer = ChatViewSerializer
    permission_classes: Tuple[Any] = (
        IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM."""
        return self.queryset.get_not_deleted().prefetch_related("members")

    def list(self, request: DRF_Request) -> DRF_Response:
        """List method for GET-request."""
#         sql = ChatMember.objects.raw(
#             "SELECT chats_chat.id, chats_chat.name, auths_customuser.id, \
# auths_customuser.slug, chats_chat.datetime_created, chats_chat.photo, chats_chat.datetime_deleted, chats_chatmember.chat_name FROM chats_chatmember \
# JOIN chats_chat ON chats_chat.id = chats_chatmember.chat_id JOIN \
# auths_customuser ON auths_customuser.id = chats_chatmember.user_id"
#         )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            # data=sql,
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def retrieve(self, request: DRF_Request, pk: int = 0) -> DRF_Response:
        """Handle GET-request with ID to show users phones."""
        chat: Optional[Chat] = None
        try:
            chat = self.get_queryset().get(id=pk)
        except Chat.DoesNotExist:
            return DRF_Response(
                {'response': 'Не нашел такой чат'}
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=chat,
            serializer_class=self.serializer_class,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ):  # noqa
        my_data: QueryDict = request.data.copy()
        my_data["slug"] = slugify(
            my_data["slug"]
        )
        my_data["owner"] = request.user.id
        # breakpoint()
        # my_data["members"] = [request.user]

        serializer: ChatCreateSerializer = ChatCreateSerializer(
            data=my_data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
