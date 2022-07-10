from typing import (
    Any,
    Optional,
    Tuple,
    Dict,
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
from abstracts.handlers import (
    NoneDataHandler,
)
from news.models import (
    Tag,
    Category,
)
from news.serializers import (
    TagBaseModelSerializer,
    TagDetailSerializer,
    CategoryBaseModelSerializer,
    CategoryDetailSerializer,
)


class TagViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """TagViewSet."""

    queryset: QuerySet[Tag] = \
        Tag.objects.all()
    serializer_class: TagBaseModelSerializer = TagBaseModelSerializer
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
        """Handle GET-request to see all tags."""
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
        """Handle GET-request with specified ID."""
        is_deleted: bool = request.data.get("is_deleted", False)
        if not is_deleted:
            is_deleted = kwargs.get("is_deleted", False)

        tag: Optional[Tag] = self.get_instance_by_id(
            Tag,
            pk=pk,
            is_deleted=is_deleted
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=tag,
            message=f"Тэг с ID {pk} не найден или был удалён",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            response = self.get_drf_response(
                request=request,
                data=tag,
                serializer_class=TagDetailSerializer
            )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new Tag."""
        serializer: TagBaseModelSerializer = TagBaseModelSerializer(
            data=request.data
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_tag: Tag = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_tag,
                serializer_class=self.serializer_class
            )
            return response

        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT-request with provided ID."""
        is_partial: bool = kwargs.get("pk", False)

        pk: Optional[str] = kwargs.get('pk', None)
        response: Optional[DRF_Response] = self.get_none_response(
            object=pk,
            message="Первичный ключ должен быть предоставлен",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        instance: Optional[Tag] = self.get_instance_by_id(
            class_name=Tag,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такой ТЭГ с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: TagBaseModelSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_tag: Tag = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_tag,
            serializer_class=TagDetailSerializer
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


class CategoryViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """CategoryViewSet."""

    queryset: QuerySet[Category] = \
        Category.objects.all()
    serializer_class: CategoryBaseModelSerializer = CategoryBaseModelSerializer
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
        """Handle GET-request to see all non-deleted categories."""
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
        """Handle GET-request with provided PK (ID)."""
        is_deleted: bool = request.data.get("is_deleted", False)
        if not is_deleted:
            is_deleted = kwargs.get("is_deleted", False)

        category: Optional[Category] = self.get_instance_by_id(
            class_name=Category,
            pk=pk,
            is_deleted=is_deleted
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=category,
            message=f"Категория с ID {pk} не найдена или была удалена",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            response = self.get_drf_response(
                request=request,
                data=category,
                serializer_class=CategoryDetailSerializer
            )
        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new Category."""
        serializer: CategoryBaseModelSerializer = self.serializer_class(
            data=request.data
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_category: Category = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_category,
                serializer_class=self.serializer_class
            )
            return response

        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT-request with provided ID."""
        is_partial: bool = kwargs.get("pk", False)

        pk: Optional[str] = kwargs.get('pk', None)
        response: Optional[DRF_Response] = self.get_none_response(
            object=pk,
            message="Первичный ключ должен быть предоставлен",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        instance: Optional[Category] = self.get_instance_by_id(
            class_name=Category,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Категория с ID: {pk} не найдена или удалена',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: CategoryBaseModelSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_category: Category = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_category,
            serializer_class=CategoryDetailSerializer
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
