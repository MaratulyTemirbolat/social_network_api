from typing import (
    Any,
    Optional,
    Tuple,
    Dict,
    List,
)

from django.db.models import (
    QuerySet,
    Model,
)
from django.http.request import QueryDict

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
from news.models import (
    Tag,
    Category,
    News,
)
from news.serializers import (
    TagBaseModelSerializer,
    TagDetailSerializer,
    CategoryBaseModelSerializer,
    CategoryDetailSerializer,
    NewsBaseSerializer,
    NewsListSerializer,
    NewsDetailSerializer,
    NewsCreateSerializer,
    NewsUpdateSerializer,
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
        is_partial: bool = kwargs.get("is_partial", False)

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


class NewsViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """NewsViewSet."""

    queryset: QuerySet[News] = \
        News.objects.all()
    serializer_class: NewsBaseSerializer = NewsBaseSerializer
    permission_classes: Tuple[Any] = (
        IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted().\
            select_related("author", "group", "category")

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
            return obj.select_related(
                "group",
                "author",
                "category"
            ).prefetch_related("liked_users").get(pk=pk)
        except class_name.DoesNotExist:
            return None

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to get news."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=NewsListSerializer,
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

        news: Optional[News] = self.get_instance_by_id(
            class_name=News,
            pk=pk,
            is_deleted=is_deleted
        )

        response: Optional[DRF_Response] = self.get_none_response(
            object=news,
            message=f"Новость с ID {pk} не найдена или была удалена",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            response = self.get_drf_response(
                request=request,
                data=news,
                serializer_class=NewsDetailSerializer
            )
        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create News."""
        data_copy: QueryDict[str, Any] = request.data.copy()
        serializer: NewsCreateSerializer = NewsCreateSerializer(
            data=data_copy
        )
        valid: bool = serializer.is_valid()
        if valid:
            news: News = serializer.save()
            news = self.get_instance_by_id(
                class_name=News,
                pk=news.id
            )

            response: Optional[DRF_Response] = None

            tags: list[int] = data_copy.get("tags", None)
            if tags and isinstance(tags, list):
                response = self.add_tags(
                    request=request,
                    news=news,
                    tags=tags
                )
            else:
                response = self.get_drf_response(
                    request=request,
                    data=news,
                    serializer_class=NewsDetailSerializer
                )
            return response

        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_tags(
        self,
        request: DRF_Request,
        news: News,
        tags: List[int],
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Add tags to the news."""
        existed_tags: AbstractDateTimeQuerySet = \
            Tag.objects.get_not_deleted()\
            .filter(id__in=tags)

        cur_tag: Tag
        for cur_tag in existed_tags:
            news.tags.add(cur_tag)

        return self.get_drf_response(
            request=request,
            data=news,
            serializer_class=NewsDetailSerializer
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

        instance: Optional[News] = self.get_instance_by_id(
            class_name=News,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Новость с ID: {pk} не найдена или удалена',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: NewsUpdateSerializer = NewsUpdateSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_news: News = serializer.save()
        updated_news = self.get_instance_by_id(
            class_name=News,
            pk=updated_news.id
        )

        return self.get_drf_response(
            request=request,
            data=updated_news,
            serializer_class=NewsDetailSerializer
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
