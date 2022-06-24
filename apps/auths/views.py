from typing import (
    Optional,
)
from datetime import datetime

from rest_framework import (
    permissions,
)
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRF_Response
from rest_framework.request import Request as DRF_Request
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from django.db.models import QuerySet

from auths.models import (
    CustomUser,
    # Friends,
    Phone,
)
from auths.serializers import (
    CustomUserSerializer,
    # FriendsSerializer,
    PhoneSerializer,
)
from abstracts.paginators import (
    AbstractPageNumberPaginator,
)
from abstracts.handlers import DRFResponseHandler


class CustomUserViewSet(DRFResponseHandler, ViewSet):
    """
    ViewSet for CustomUser.

    * Does-not equire token authentication.
    * Only superusers are able to access this view.
    """

    # authentication_classes: tuple = (
    #     authentication.TokenAuthentication,
    # )
    permission_classes: tuple = (
        permissions.IsAdminUser,
    )
    queryset: QuerySet[CustomUser] = \
        CustomUser.objects.get_not_deleted()
    serializer_class: CustomUserSerializer = CustomUserSerializer

    def get_queryset(self) -> QuerySet[CustomUser]:  # noqa
        return self.queryset.filter(
            is_superuser=False
        )

    @action(
        methods=["get"],
        detail=False,
        url_path="all_admins",
        permission_classes=(
            permissions.AllowAny,
        )
    )
    def get_administrators(self, request: DRF_Request) -> DRF_Response:
        """Handle POST-request to show custom-info about custom_users."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.queryset.filter(is_superuser=True),
            serializer_class=self.serializer_class,
            many=True
        )
        return response

    def list(self, request: DRF_Request) -> DRF_Response:
        """Return list of all users."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.queryset,
            serializer_class=self.serializer_class,
            many=True
        )

        return response

    def create(self, request: DRF_Request) -> DRF_Response:
        """Handle POST-request to show custom_users."""
        serializer: CustomUserSerializer = \
            CustomUserSerializer(
                data=request.data
            )
        if serializer.is_valid():
            serializer.save()
            return DRF_Response(
                {'data': f'Объект {serializer.id} создан'}
            )
        return DRF_Response(
            {'response': 'Объект не создан'}
        )

    def retrieve(self, request: DRF_Request, pk: int = 0) -> DRF_Response:
        """Handle GET-request with ID to show custom_user."""
        # Retrieving certain object
        #
        custom_user: Optional[CustomUser] = None
        try:
            custom_user = self.get_queryset().get(
                id=pk
            )
        except CustomUser.DoesNotExist:
            return DRF_Response(
                {'response': 'Не нашел такого юзера'}
            )

        serializer: CustomUserSerializer = \
            CustomUserSerializer(
                custom_user
            )

        return DRF_Response(
            {'response': serializer.data}
        )

    def partial_update(
        self,
        request: DRF_Request,
        pk: int = 0
    ) -> DRF_Response:
        """Handle PATCH-request with ID to show custom_user."""
        return DRF_Response(
            {'response': 'Метод partial_update'}
        )

    def update(self, request: DRF_Request) -> DRF_Response:
        """Handle PUT-request with ID to show custom_user."""
        return DRF_Response(
            {'response': 'Метод update'}
        )

    def destroy(self, request: DRF_Request, pk: int = 0) -> DRF_Response:
        """Handle DELETE-request with ID to show custom_user."""
        custom_user: Optional[CustomUser] = None
        try:
            custom_user = self.get_queryset().get(
                id=pk
            )
        except CustomUser.DoesNotExist:
            return DRF_Response(
                {'data': f'Объект с ID: {pk} не найден'}
            )

        custom_user.datetime_deleted = datetime.now()
        custom_user.save(
            update_fields=['datetime_deleted']
        )
        return DRF_Response(
            {'data': f'Объект {custom_user.id} удален'}
        )


class CustomUserViewSetTrial(DRFResponseHandler, ViewSet):  # noqa
    permission_classes: tuple = (
        permissions.AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator
    queryset: QuerySet[CustomUser] = \
        CustomUser.objects.get_not_deleted()
    serializer_class: CustomUserSerializer = CustomUserSerializer

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[CustomUser]:
        """Obtain the class instance by primary key."""
        user: Optional[CustomUser] = None
        try:
            user = self.get_queryset().get(id=pk)
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_queryset(self) -> QuerySet[CustomUser]:
        """Get not_deleted users."""
        return self.queryset

    def list(
        self,
        request: DRF_Request
    ) -> DRF_Response:
        """Return list of all users."""
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
        pk: int = 0
    ) -> DRF_Response:
        """Process GET: /pk response for k-th user."""
        user: Optional[CustomUser] = self.get_instance(pk=pk)
        if not user:
            return DRF_Response(
                data={
                    "response": f"Данный пользователь не найден с pk={pk}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=user,
            serializer_class=self.serializer_class,
            many=False
        )
        return response


# ПРОБЛЕМЫ
class PhoneViewSet(DRFResponseHandler, ViewSet):
    """PhoneViewset."""

    # permission_classes: tuple = (
    #     permissions.IsAuthenticated,
    # )
    permission_classes: tuple = (
        permissions.AllowAny,
    )
    queryset: QuerySet[Phone] = \
        Phone.objects.all()
    serializer_class: PhoneSerializer = PhoneSerializer
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet[Phone]:  # noqa
        return self.queryset.get_not_deleted()

    @action(
        methods=["get"],
        detail=False,
        url_path="deleted_phones",
        permission_classes=(
            permissions.AllowAny,
        )
    )
    def get_deleted_phones(self, request: DRF_Request) -> DRF_Response:
        """Handle POST-request to show custom-info about custom_users."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.queryset.get_deleted(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def list(self, request: DRF_Request) -> DRF_Response:
        """Return list of all non-deleted phones."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )

        return response

    def retrieve(self, request: DRF_Request, pk: int = 0) -> DRF_Response:
        """Handle GET-request with ID to show users phones."""
        # Retrieving certain object
        #
        phone: Optional[Phone] = None
        try:
            phone = self.queryset.get(
                id=pk
            )
        except Phone.DoesNotExist:
            return DRF_Response(
                {'response': 'Не нашел такой телефон'}
            )
        if phone.datetime_deleted:
            return DRF_Response(
                {'response': 'Данный телефон удален'}
            )
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=phone,
            serializer_class=self.serializer_class,
            many=False
        )
        return response

    # НЕ РАБОТАЕТ
    def create(self, request: DRF_Request) -> DRF_Response:
        """Handle POST-request to show custom_users."""
        sent_data: dict = request.data.copy()
        # sent_data["owner"] = request.user
        sent_data["datetime_created"] = datetime.now()
        # breakpoint()
        serializer: PhoneSerializer = \
            self.serializer_class(
                data=request.data
            )
        breakpoint()
        if serializer.is_valid():
            serializer.save()
            return DRF_Response(
                {'data': f'Объект {serializer.id} создан'}
            )
        return DRF_Response(
            {'response': 'Объект не создан'}
        )

    def destroy(self, request: DRF_Request, pk: int = 0) -> DRF_Response:
        """Handle DELETE-request with ID to show custom_user."""
        phone: Optional[Phone] = None
        try:
            phone = self.get_queryset().get(
                id=pk
            )
        except Phone.DoesNotExist:
            return DRF_Response(
                {'data': f'Объект с ID: {pk} не найден'}
            )

        phone.delete()
        return DRF_Response(
            {'data': f'Телефон {phone.phone} удален'}
        )

    def update(self, request: DRF_Request, pk: int = None) -> DRF_Response:
        """Handle PUT-request with ID to show custom_user."""
        return DRF_Response(
            {'response': 'Метод update'}
        )

    def partial_update(
        self,
        request: DRF_Request,
        pk: int = 0
    ) -> DRF_Response:
        """Handle PATCH-request with ID to show custom_user."""
        return DRF_Response(
            {'response': 'Метод partial_update'}
        )


class TrialApiView(ListCreateAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
