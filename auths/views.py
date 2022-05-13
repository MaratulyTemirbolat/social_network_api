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

from django.db.models import QuerySet

from auths.models import CustomUser
from auths.serializers import CustomUserSerializer
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
        CustomUser.objects.get_non_deleted()
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
