from typing import (
    Optional,
    Tuple,
    Any,
    Dict,
)
from datetime import datetime

from django.db.models import (
    Model,
    QuerySet,
)


from rest_framework.serializers import (
    SerializerMethodField,
    DateTimeField,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.pagination import BasePagination
from rest_framework import status

from abstracts.models import AbstractDateTime
from abstracts.handlers import DRFResponseHandler


class AbstractDateTimeSerializerMixin:
    """AbstractDateTimeSerializer."""

    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )
    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )

    def get_is_deleted(self, obj: AbstractDateTime) -> bool:
        """Resolution of is_deleted variable."""
        if obj.datetime_deleted:
            return True
        return False


class ModelInstanceMixin:
    """Mixin for getting instance that are inherited from Model."""

    def get_instance_by_id(
        self,
        class_name: Model,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[Model]:
        """Obtain the class instance by primary key."""
        obj: Optional[Model] = None
        try:
            if not is_deleted:
                obj = class_name.objects.get_not_deleted()
            else:
                obj = class_name.objects.get_deleted()
            return obj.get(pk=pk)
        except class_name.DoesNotExist:
            return None

    def get_queryset_instance_by_id(
        self,
        class_name: Model,
        queryset: QuerySet,
        pk: int = 0,
    ) -> Optional[Model]:
        """Get class instance by PK with provided queryset."""
        obj: Optional[Model] = None
        try:
            obj = queryset.get(pk=pk)
            return obj
        except class_name.DoesNotExist:
            return None


class DeletedRequestMixin(DRFResponseHandler):
    """AbstractDateTimeViewSet."""

    queryset: Optional[QuerySet]
    serializer_class: Optional[Any]
    pagination_class: Optional[BasePagination]

    @action(
        methods=["get"],
        detail=False,
        url_path="deleted",
        permission_classes=(
            IsAdminUser,
        )
    )
    def get_deleted_objects(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Get all deleted chats."""
        if not self.queryset or \
            not self.serializer_class or \
                not self.pagination_class:
            return DRF_Response(
                data={"response": "Не все поля реализованы во ViewSet"},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.queryset.get_deleted(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )
        return response
