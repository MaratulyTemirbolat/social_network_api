"""ViewSets or ApiViews for Complains app."""

from typing import (
    Tuple,
    Any,
    Dict,
    Optional,
)

from django.db.models import QuerySet

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework import status

from complains.models import (
    ComplainReason,
    ComplainNews,
)
from complains.serializers import (
    ComplainReasonSerializer,
    ComplainNewsBaseSerializer,
    ComplainNewsDetailSerializer,
)
from abstracts.handlers import (
    DRFResponseHandler,
    NoneDataHandler,
)
from abstracts.paginators import AbstractPageNumberPaginator


class ComplainReasonViewSet(NoneDataHandler, DRFResponseHandler, ViewSet):
    """ComplainReasonViewSet."""

    queryset: QuerySet[ComplainReason] = \
        ComplainReason.objects.all()
    serializer_class: ComplainReasonSerializer = ComplainReasonSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted()

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[ComplainReason]:
        """Obtain the class instance by primary key."""
        compl_reason: Optional[ComplainReason] = None
        try:
            compl_reason = self.get_queryset().get(id=pk)
            return compl_reason
        except ComplainReason.DoesNotExist:
            return None

    @action(
        methods=["get"],
        detail=False,
        url_path="deleted_reasons",
        permission_classes=(
            IsAuthenticated,
        )
    )
    def get_deleted_complains(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """View (Get) all deleted reasons."""
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
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """List method for non-deleted reasons (GET-request)."""
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
        """Handle GET-request with ID to complain reason."""
        compl_reason: Optional[ComplainReason] = self.get_instance(pk=pk)
        if not compl_reason:
            return DRF_Response(
                {'response': 'Не нашел такой чат'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=compl_reason,
            serializer_class=self.serializer_class,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request."""
        serializer: ComplainReasonSerializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT method with provided id."""
        is_partial: bool = kwargs.pop('is_partial', False)

        pk: Optional[str] = kwargs.get('pk', None)
        response: Optional[DRF_Response] = self.get_none_response(
            object=pk,
            message="Первичный ключ должен быть предоставлен",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        instance: Optional[ComplainReason] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую причину жалобы с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: ComplainReasonSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(data=serializer.data)

    def partial_update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.update(request, *args, **kwargs)


# Реализовать
class ComplainNewsViewSet(NoneDataHandler, DRFResponseHandler, ViewSet):
    """ComplainNewsViewSet."""

    queryset: QuerySet[ComplainNews] = \
        ComplainNews.objects.all()
    serializer_class: ComplainNewsBaseSerializer = ComplainNewsBaseSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted()

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[ComplainNews]:
        """Obtain the class instance by primary key."""
        compl_news: Optional[ComplainNews] = None
        try:
            compl_news = self.get_queryset().get(id=pk)
            return compl_news
        except ComplainNews.DoesNotExist:
            return None

    @action(
        methods=["get"],
        detail=False,
        url_path="deleted_news_complains",
        permission_classes=(
            IsAuthenticated,
        )
    )
    def get_deleted_news_complains(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """View (Get) all deleted news complains."""
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
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """List method for non-deleted news complains (GET-request)."""
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
        """Handle GET-request with ID to complain reason."""
        compl_news: Optional[ComplainNews] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=compl_news,
            message="Не нашел такой жалобу на новость",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        response = self.get_drf_response(
            request=request,
            data=compl_news,
            serializer_class=ComplainNewsDetailSerializer,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request."""
        serializer: ComplainNewsBaseSerializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT method with provided id."""
        is_partial: bool = kwargs.pop('is_partial', False)

        pk: Optional[str] = kwargs.get('pk', None)
        response: Optional[DRF_Response] = self.get_none_response(
            object=pk,
            message="Первичный ключ должен быть предоставлен",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        instance: Optional[ComplainNews] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую новостную жалобу с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: ComplainNewsBaseSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(data=serializer.data)

    def partial_update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.update(request, *args, **kwargs)
