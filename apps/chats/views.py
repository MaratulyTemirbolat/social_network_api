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
)
from rest_framework.decorators import action
from rest_framework import status

from chats.models import (
    Chat,
)
from chats.serializers import (
    ChatCreateSerializer,
    ChatViewSerializer,
    ChatViewSingleSerializer,
)
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator


class ChatViewSet(DRFResponseHandler, ViewSet):
    """Chat class ViewSet."""

    queryset: QuerySet[Chat] = \
        Chat.objects.all()
    serializer_class: ChatViewSerializer = ChatViewSerializer
    permission_classes: Tuple[Any] = (
        # IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[Chat]:
        """Obtain the class instance by primary key."""
        chat: Optional[Chat] = None
        try:
            chat = self.get_queryset().get(id=pk)
            return chat
        except Chat.DoesNotExist:
            return None

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM."""
        return self.queryset.get_not_deleted().prefetch_related(
            "members"
        ).select_related("owner")

    @action(
        methods=["get"],
        detail=False,
        url_path="deleted_chats",
        permission_classes=(
            IsAdminUser,
        )
    )
    def get_deleted_chats(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Get all deleted chats."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.queryset.get_deleted(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def list(
        self,
        request: DRF_Request
    ) -> DRF_Response:
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

    def retrieve(
        self,
        request: DRF_Request,
        pk: int = 0
    ) -> DRF_Response:
        """Handle GET-request with ID to show users phones."""
        chat: Optional[Chat] = self.get_instance(pk=pk)
        if not chat:
            return DRF_Response(
                {'response': 'Не нашел такой чат'}
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=chat,
            serializer_class=ChatViewSingleSerializer,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:  # noqa
        my_data: QueryDict = request.data.copy()
        my_data["slug"] = slugify(
            my_data["slug"]
        )
        my_data["owner"] = request.user.id

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

    def partial_update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.update(request, *args, **kwargs)

    def update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT method with provided id."""
        is_partial: bool = kwargs.pop('is_partial', False)

        pk: Optional[str] = kwargs.get('pk', None)
        if not pk:
            return DRF_Response(
                {"response": "Первичный ключ должен быть предоставлен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance: Optional[Chat] = self.get_instance(pk=pk)
        if not instance:
            return DRF_Response(
                {'response': 'Не нашел такой чат'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer: ChatCreateSerializer = ChatCreateSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(data=serializer.data)
