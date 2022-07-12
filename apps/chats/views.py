from typing import (
    Any,
    Optional,
    Tuple,
    Dict,
    Set,
    List,
)

from django.db.models import QuerySet
from django.utils.text import slugify
from django.http.request import QueryDict

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework import status

from auths.models import CustomUser
from chats.models import (
    Chat,
    ChatMember,
)
from chats.serializers import (
    ChatBaseModelSerializer,
    ChatListSerializer,
    ChatDetailSerializer,
    ChatUpdateSerializer,
)
from chats.permissions import (
    IsMemberOrAdmin,
    IsOwnerOrAdmin,
)
from abstracts.handlers import (
    NoneDataHandler,
    DRFResponseHandler,
)
from abstracts.paginators import AbstractPageNumberPaginator
from abstracts.mixins import (
    ModelInstanceMixin,
    DeletedRequestMixin,
)


class ChatViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """Chat class ViewSet."""

    queryset: QuerySet[Chat] = \
        Chat.objects.all()
    serializer_class: ChatBaseModelSerializer = ChatBaseModelSerializer
    permission_classes: Tuple[Any] = (
        IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM."""
        # return self.queryset.get_not_deleted().prefetch_related(
        #     "chatmember_set"
        # ).select_related("owner")
        return self.queryset.get_not_deleted().select_related("owner")

    @action(
        methods=["get"],
        detail=False,
        url_path="all",
        permission_classes=(
            IsAdminUser,
        )
    )
    def get_all_chats(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """List method for GET-request."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to see all non-deleted user chats."""
        chats: QuerySet[Chat] = request.user.joined_chats.get_not_deleted()\
            .select_related("owner")\
            .prefetch_related("members")
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=chats,
            serializer_class=ChatListSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    @action(
        methods=["get"],
        detail=True,
        url_path="view",
        permission_classes=(
            IsMemberOrAdmin,
        )
    )
    def view_chat(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with ID to show users phones."""
        chat: Optional[Chat] = None

        chat = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=chat,
            message=f"Чат с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=chat
            )
            response = self.get_drf_response(
                request=request,
                data=chat,
                serializer_class=ChatDetailSerializer
            )
        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new Chat."""
        data_copy: QueryDict = request.data.copy()

        slug: Optional[str] = data_copy.get("slug", None)
        if not slug or not isinstance(slug, str):
            return DRF_Response(
                data={
                    "response": "Поле 'slug' неправильно заполнено"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data_copy["slug"] = slugify(data_copy["slug"])

        serializer: ChatBaseModelSerializer = self.serializer_class(
            data=data_copy,
            context={"request": request}
        )

        valid: bool = serializer.is_valid()
        if valid:
            new_chat: Chat = serializer.save()
            return self.get_drf_response(
                request=request,
                data=new_chat,
                serializer_class=ChatDetailSerializer
            )
        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["patch"],
        detail=True,
        url_path="edit",
        permission_classes=(
            IsOwnerOrAdmin,
        )
    )
    def edit_chat(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.full_chat_edit(request, pk, *args, **kwargs)

    @action(
        methods=["put"],
        detail=True,
        url_path="full_edit",
        permission_classes=(
            IsOwnerOrAdmin,
        )
    )
    def full_chat_edit(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT method with provided id."""
        is_partial: bool = kwargs.pop('is_partial', False)

        instance: Optional[Chat] = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f"Чат с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        self.check_object_permissions(
            request=request,
            obj=instance
        )

        serializer: ChatUpdateSerializer = ChatUpdateSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="add_members",
        permission_classes=(
            IsOwnerOrAdmin,
        )
    )
    def add_friends(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Any,
        **kwargs: Any
    ) -> DRF_Response:
        """POST-request for friends adding to the chat."""
        chat: Optional[Chat] = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset().prefetch_related("chatmember_set"),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=chat,
            message=f"Чат с ID {pk} не найдена, либо она удалена",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        self.check_object_permissions(
            request=request,
            obj=chat
        )

        chat_members_id: QuerySet = chat.members.values_list("id", flat=True)
        required_members: Optional[List[int]] = request.data.get(
            "members", None
        )
        response = self.get_none_response(
            object=required_members,
            message="Необходимо предоставить пользователей",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        member_difference: Set[int] = (
            set(required_members) - set(chat_members_id)
        )
        resulted_members: QuerySet = CustomUser.objects.get_not_deleted().\
            filter(id__in=member_difference).values_list(
                "id",
                "username"
            )

        added_people: List[ChatMember] = []

        resulted_members_number: int = resulted_members.count()
        i: int
        for i in range(resulted_members_number):
            added_people.append(
                ChatMember(
                    chat_id=chat.id,
                    user_id=resulted_members[i][0],
                    chat_name=resulted_members[i][1]
                )
            )
        ChatMember.objects.bulk_create(added_people)

        if resulted_members_number > 0:
            return DRF_Response(
                data={
                    "response": "Все возможные пользователи добавлены"
                },
                status=status.HTTP_200_OK
            )
        return DRF_Response(
            data={
                "response": "Никто из данных пользователей не добавлен"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="remove_members",
        permission_classes=(
            IsOwnerOrAdmin,
        )
    )
    def remove_friends(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Any,
        **kwargs: Any
    ) -> DRF_Response:
        """POST-request to remove friends from chat by id."""
        chat: Optional[Chat] = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset().prefetch_related("chatmember_set"),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=chat,
            message=f"Чат с ID {pk} не найдена, либо он удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        self.check_object_permissions(
            request=request,
            obj=chat
        )

        required_members: Optional[List[int]] = request.data.get(
            "members", None
        )
        response = self.get_none_response(
            object=required_members,
            message="Необходимо предоставить пользователей",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        ChatMember.objects.filter(
            chat_id=chat.id,
            user_id__in=required_members
        ).delete()

        response = DRF_Response(
            data={
                "response": "Все возможные пользователи удалены!"
            },
            status=status.HTTP_200_OK
        )

        return response

    @action(
        methods=["delete"],
        detail=True,
        url_path="drop",
        permission_classes=(
            IsOwnerOrAdmin,
        )
    )
    def delete_chat(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle DELETE-request to drop owned chat."""
        chat: Optional[Chat] = None

        chat = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=chat,
            message=f"Чат с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=chat
            )
            chat_name: str = chat.name
            chat.delete()
            response = DRF_Response(
                data={
                    "response": f"Чат {chat_name} успешно удалён"
                },
                status=status.HTTP_200_OK
            )
        return response

    @action(
        methods=["delete"],
        detail=True,
        url_path="leave",
        permission_classes=(
            IsMemberOrAdmin,
        )
    )
    def leave_chat(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle DELETE-request to leave current chat."""
        chat: Optional[Chat] = None

        chat = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=chat,
            message=f"Чат с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=chat
            )
            ChatMember.objects.get(
                chat_id=chat.id,
                user_id=request.user.id
            ).delete()
            response = DRF_Response(
                data={
                    "response": "Вы успешно покинули чат",
                },
                status=status.HTTP_200_OK
            )
        return response

    @action(
        methods=["patch"],
        detail=True,
        url_path="edit_chat_name",
        permission_classes=(
            IsMemberOrAdmin,
        )
    )
    def change_chat_name(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH-request to change name in the chat."""
        chat_name: Optional[str] = request.data.get("chat_name", None)
        if not chat_name or not isinstance(chat_name, str):
            return DRF_Response(
                data={
                    "response": "Поле 'chat_name' должно быть предоставлено"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        chat: Optional[Chat] = None

        chat = self.get_queryset_instance_by_id(
            class_name=Chat,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=chat,
            message=f"Чат с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=chat
            )
            chat_member: ChatMember = ChatMember.objects.get(
                chat_id=chat.id,
                user_id=request.user.id
            )
            old_name: str = chat_member.chat_name
            if old_name == chat_name:
                return DRF_Response(
                    data={
                        "response": "Никнейм идентичен старому. ТАК НЕЛЬЗЯ!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            chat_member.chat_name = chat_name
            chat_member.save(
                update_fields=['chat_name']
            )

            response = DRF_Response(
                data={
                    "response": f"Вы изменили ник с {old_name} на {chat_name}",
                },
                status=status.HTTP_200_OK
            )
        return response
