from typing import (
    Optional,
    Any,
    Tuple,
    Dict,
)
from datetime import datetime

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRF_Response
from rest_framework.request import Request as DRF_Request
from rest_framework import status

from django.db.models import QuerySet, Q

from auths.permissions import (
    IsOwnerOrAdmin,
    IsPhoneOwnerOrAdmin,
)
from auths.models import (
    CustomUser,
    Friends,
    Phone,
    CustomUserManager,
)
from auths.tools import (
    is_superuser_authenticated,
    get_friends_drf_response,
)
from auths.serializers import (
    PhoneBaseSerializer,
    CustomUserBaseSerializer,
    CustomUserDetailSerializer,
    PhoneDetailSerializer,
)
from abstracts.paginators import (
    AbstractPageNumberPaginator,
)
from abstracts.mixins import (
    ModelInstanceMixin,
    DeletedRequestMixin,
)
from abstracts.handlers import NoneDataHandler


class CustomUserViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """
    ViewSet for CustomUser.

    * Does-not equire token authentication.
    * Only superusers are able to access this view.
    """

    # authentication_classes: tuple = (
    #     authentication.TokenAuthentication,
    # )
    permission_classes: tuple = (
        permissions.IsAuthenticated,
    )
    queryset: CustomUserManager = \
        CustomUser.objects
    serializer_class: CustomUserBaseSerializer = CustomUserBaseSerializer
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet[CustomUser]:
        """Get not deleted users."""
        return self.queryset.get_not_deleted()

    @action(
        methods=["get"],
        detail=False,
        url_path="admins",
        permission_classes=(
            permissions.IsAdminUser,
        )
    )
    def get_administrators(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to show custom-info about custom_users."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.queryset.get_active_administrators(),
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
        """Handle GET-request to return list of all users."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )

        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with ID to show custom_user."""
        is_deleted: bool = request.data.get("is_deleted", False)
        if not is_deleted:
            is_deleted = kwargs.get("is_deleted", False)

        custom_user: Optional[CustomUser] = None
        queryset: QuerySet[CustomUser]

        if not is_deleted:
            queryset = self.get_queryset()
        else:
            queryset = self.queryset.get_deleted()
        custom_user = self.get_queryset_instance_by_id(
            class_name=CustomUser,
            queryset=queryset.prefetch_related("phones"),
            pk=pk
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=custom_user,
            message=f"Пользователь с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            is_blocked: bool = Friends.objects.filter(
                from_user=custom_user,
                to_user=request.user,
                is_blocked=True
            ).exists()
            if is_blocked:
                return DRF_Response(
                    data={
                        "response": f"Вы заблокированы {custom_user.username}"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            response = self.get_drf_response(
                request=request,
                data=custom_user,
                serializer_class=CustomUserDetailSerializer
            )
        return response

    @action(
        methods=["post"],
        detail=False,
        url_path="create_user",
        permission_classes=(
            permissions.AllowAny,
        )
    )
    def create_user(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to show custom_users."""
        is_superuser: bool = kwargs.get(
            "is_superuser",
            False
        )
        is_staff: bool = False

        if is_superuser and \
                not is_superuser_authenticated(request.user):
            return DRF_Response(
                data={
                    "response": "Вы не админ, чтобы создать супер пользователя"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer: CustomUserBaseSerializer = self.serializer_class(
            data=request.data
        )

        new_password: Optional[str] = request.data.get("password", None)

        if not new_password or not isinstance(new_password, str):
            return DRF_Response(
                data={
                    "password": "Пароль обязан быть в формате строки"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        valid: bool = serializer.is_valid()
        if valid:
            if is_superuser:
                is_staff = True

            new_custom_user: CustomUser = serializer.save(
                is_superuser=is_superuser,
                is_staff=is_staff,
                password=new_password
            )
            new_custom_user.set_password(new_password)
            new_custom_user.save()
            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_custom_user,
                serializer_class=self.serializer_class
            )
            return response
        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["post"],
        detail=False,
        url_path="create_superuser",
        permission_classes=(
            permissions.IsAdminUser,
        )
    )
    def create_superuser(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request for superuser creation."""
        kwargs['is_superuser'] = True
        return self.create_user(request, *args, **kwargs)

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
        """Handle PUT-request with provided ID."""
        is_partial: bool = kwargs.get("is_partial", False)

        pk: Optional[str] = kwargs.get('pk', None)
        response: Optional[DRF_Response] = self.get_none_response(
            object=pk,
            message="Первичный ключ должен быть предоставлен",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        instance: Optional[CustomUser] = self.get_queryset_instance_by_id(
            class_name=CustomUser,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такого пользователя с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: CustomUserBaseSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_video: CustomUser = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_video,
            serializer_class=CustomUserDetailSerializer
        )

    @action(
        methods=["delete"],
        detail=True,
        url_path="delete_user",
        permission_classes=(
            IsOwnerOrAdmin,
        )
    )
    def delete_user(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle DELETE-request with ID to show custom_user."""
        custom_user: Optional[CustomUser] = None

        custom_user = self.get_queryset_instance_by_id(
            class_name=CustomUser,
            queryset=self.get_queryset(),
            pk=pk
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=custom_user,
            message=f"Пользователь с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=custom_user
            )
            custom_user.delete()
            custom_user.is_active = False
            custom_user.save(
                update_fields=['is_active']
            )
            response = DRF_Response(
                {'data': f'Пользователь {custom_user.id} удален'},
                status=status.HTTP_200_OK
            )

        return response

    @action(
        methods=["post"],
        detail=True,
        url_path="add_friend",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def add_friend(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Add user to the friends."""
        custom_user: Optional[CustomUser] = None

        custom_user = self.get_queryset_instance_by_id(
            class_name=CustomUser,
            queryset=self.get_queryset(),
            pk=pk
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=custom_user,
            message=f"Пользователь с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            if request.user == custom_user:
                return DRF_Response(
                    data={
                        "response": "Вы не можете добавить себя же в друзья"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            friends_exist_state: Optional[int] = Friends.objects.get_friends_state(
                from_user=request.user,
                to_user=custom_user
            )
            if not friends_exist_state:
                Friends.objects.create(
                    from_user=request.user,
                    to_user=custom_user
                )
            response = get_friends_drf_response(
                friends_state=friends_exist_state,
                targer_username=custom_user.username
            )

        return response

    @action(
        methods=["post"],
        detail=True,
        url_path="unblock_block_user",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def unblock_block_user(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to block or unblock user."""
        custom_user: Optional[CustomUser] = None

        custom_user = self.get_queryset_instance_by_id(
            class_name=CustomUser,
            queryset=self.get_queryset(),
            pk=pk
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=custom_user,
            message=f"Пользователь с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            if request.user == custom_user:
                return DRF_Response(
                    data={
                        "response": "Вы не можете взаимодействовать с собой"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            block: bool = request.data.get("block", True)
            if not isinstance(block, bool):
                return DRF_Response(
                    data={
                        "response": "Поле 'block' в body заполнен неправильно"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            kwargs["to_user"] = custom_user
            if block:
                response = self.__block_user(request, *args, **kwargs)
            else:
                response = self.__unblock_user(request, *args, **kwargs)
        return response

    def __block_user(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Block user."""
        to_user: CustomUser = kwargs["to_user"]
        friends: Optional[Friends] = Friends.objects.get_friends(
            from_user=request.user,
            to_user=to_user
        )
        if not friends:
            Friends.objects.create(
                from_user=request.user,
                to_user=to_user,
                is_blocked=True
            )
            return DRF_Response(
                data={
                    "response": f"Вы успешно заблокировали {to_user.username}"
                },
                status=status.HTTP_200_OK
            )
        if friends.is_blocked:
            return DRF_Response(
                data={
                    "response": f"Вы уже блокировали {to_user.username}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        friends.is_blocked = True
        friends.save(
            update_fields=['is_blocked']
        )
        return DRF_Response(
            data={
                "response": f"Вы успешно заблокировали {to_user.username}"
            },
            status=status.HTTP_200_OK
        )

    def __unblock_user(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Unblock user."""
        to_user: CustomUser = kwargs["to_user"]
        query_exist: bool = Friends.objects.filter(
            from_user=request.user,
            to_user=to_user,
            is_blocked=True
        ).exists()
        if not query_exist:
            return DRF_Response(
                data={
                    "response": f"Вы не блокировали {to_user.username}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        Friends.objects.filter(
            Q(from_user=request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=request.user)
        ).delete()
        return DRF_Response(
            data={
                "response": f"Вы успешно разблокировали {to_user.username}"
            },
            status=status.HTTP_200_OK
        )


class PhoneViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """PhoneViewset."""

    permission_classes: tuple = (
        IsPhoneOwnerOrAdmin,
    )
    queryset: QuerySet[Phone] = \
        Phone.objects.all()
    serializer_class: PhoneBaseSerializer = PhoneBaseSerializer
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet[Phone]:
        """Get not-deleted phones."""
        return self.queryset.get_not_deleted()\
            .select_related("owner")

    @action(
        methods=["get"],
        detail=False,
        url_path="all",
        permission_classes=(
            permissions.IsAdminUser,
        )
    )
    def get_all_phones(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Return list of all non-deleted phones."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=PhoneDetailSerializer,
            many=True,
            paginator=self.pagination_class()
        )

        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with ID to show users phones."""
        is_deleted: bool = request.data.get("is_deleted", False)
        if not is_deleted:
            is_deleted = kwargs.get("is_deleted", False)

        phone: Optional[Phone] = None
        queryset: QuerySet[Phone]

        if not is_deleted:
            queryset = self.get_queryset()
        else:
            queryset = self.queryset.get_deleted()
        phone = self.get_queryset_instance_by_id(
            class_name=Phone,
            queryset=queryset,
            pk=pk
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=phone,
            message=f"Телефон с PK {pk} не найден или был удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=phone
            )
            response = self.get_drf_response(
                request=request,
                data=phone,
                serializer_class=PhoneDetailSerializer
            )
        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to show custom_users."""
        serializer: PhoneBaseSerializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_phone: Phone = serializer.save()
            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_phone,
                serializer_class=PhoneDetailSerializer
            )
            return response

        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle DELETE-request with ID to show custom_user."""
        phone: Optional[Phone] = None

        phone = self.get_queryset_instance_by_id(
            class_name=Phone,
            queryset=self.get_queryset(),
            pk=pk
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=phone,
            message=f"Телефон с PK {pk} не найден или был уже удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            self.check_object_permissions(
                request=request,
                obj=phone
            )
            phone.delete()
            response = DRF_Response(
                data={
                    "response": f"Телефон {phone.phone} успешно удалён"
                },
                status=status.HTTP_200_OK
            )
        return response

    def update(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT-request with provided ID."""
        is_partial: bool = kwargs.get("is_partial", False)

        instance: Optional[Phone] = self.get_queryset_instance_by_id(
            class_name=Phone,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел телефон с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        self.check_object_permissions(
            request=request,
            obj=instance
        )
        serializer: PhoneBaseSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        updated_video: Phone = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_video,
            serializer_class=PhoneDetailSerializer
        )

    def partial_update(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH-request with ID to show custom_user."""
        kwargs['is_partial'] = True
        return self.update(request, pk, *args, **kwargs)

    @action(
        methods=["get"],
        detail=False,
        url_path="my_phones",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def get_user_phones(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwarg: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with user id."""
        phones: QuerySet[Phone] = self.queryset.filter(
            owner=request.user
        )
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=phones,
            serializer_class=PhoneDetailSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response
