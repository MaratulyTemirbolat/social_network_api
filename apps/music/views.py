from typing import (
    Optional,
    Any,
    Tuple,
    Dict,
)

from django.db.models import (
    QuerySet,
    Model,
    Prefetch,
)

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework import status
from rest_framework.decorators import action

from music.models import (
    Music,
    Performer,
    Playlist,
)
from music.serializers import (
    PlaylistBaseSerializer,
    PlaylistDetailSerializer,
    PerformerBaseSerializer,
    PerformerDetailSerializer,
)
from abstracts.handlers import NoneDataHandler
from abstracts.paginators import AbstractPageNumberPaginator
from abstracts.mixins import (
    ModelInstanceMixin,
    DeletedRequestMixin,
)


class PlaylistViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """PlaylistViewSet."""

    queryset: QuerySet[Playlist] = \
        Playlist.objects.all()
    serializer_class: PlaylistBaseSerializer = PlaylistBaseSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_instance_by_id(
        self,
        class_name: Model,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[Model]:
        """Obtain the class instance by primary key."""
        object: Optional[Model] = None
        try:
            if not is_deleted:
                object = class_name.objects.get_not_deleted()
            else:
                object = class_name.objects.all()

            object = object.prefetch_related(
                Prefetch(
                    lookup="playlist_songs",
                    queryset=Music.objects.get_not_deleted()
                )
            ).get(pk=pk)

            return object
        except class_name.DoesNotExist:
            return None

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request for all playlists."""
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
        """Handle GET-request with provided ID."""
        is_deleted: bool = kwargs.get("is_deleted", False)

        playlist: Optional[Playlist] = self.get_instance_by_id(
            class_name=Playlist,
            pk=pk,
            is_deleted=is_deleted
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=playlist,
            message="Объект, который вы искали не найден",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        return self.get_drf_response(
            request=request,
            data=playlist,
            serializer_class=PlaylistDetailSerializer
        )

    # Нужно как то сделать с добавлением файла музыки одновременно
    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new album."""
        serializer: PlaylistBaseSerializer = self.serializer_class(
            data=request.data
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_playlist: Playlist = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_playlist,
                serializer_class=PlaylistDetailSerializer
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

        instance: Optional[Playlist] = self.get_instance_by_id(
            class_name=Playlist,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую страну с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: PlaylistBaseSerializer = PlaylistBaseSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_playlist: Playlist = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_playlist,
            serializer_class=PlaylistDetailSerializer
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

    # Реализовать после добавления END-point на Music
    @action(
        methods=["post"],
        detail=True,
        url_path="add_music",
        permission_classes=(
            IsAuthenticated,
        )
    )
    def add_music(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to add a song to the playlist."""
        return DRF_Response(
            data={
                "response": "Method is not hasn't been implemented yet."
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class PerformerViewSet(
    NoneDataHandler,
    ModelInstanceMixin,
    DeletedRequestMixin,
    ViewSet
):
    """PerformerViewSet."""

    queryset: QuerySet[Performer] = \
        Performer.objects.all()
    serializer_class: PerformerBaseSerializer = PerformerBaseSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
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
        """Handle GET-request to illustrate all performers."""
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
        is_deleted: bool = kwargs.get("is_deleted", False)

        performer: Optional[Performer] = self.get_instance_by_id(
            Performer,
            pk=pk,
            is_deleted=is_deleted
        )
        response: Optional[DRF_Response] = self.get_none_response(
            performer,
            message=f"Исполнитель с ID {pk} не был найден",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            response = self.get_drf_response(
                request=request,
                data=performer,
                serializer_class=PerformerDetailSerializer
            )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new Performer."""
        serializer: PerformerBaseSerializer = self.serializer_class(
            data=request.data
        )

        valid: bool = serializer.is_valid()
        if valid:
            new_performer: Performer = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_performer,
                serializer_class=PerformerDetailSerializer
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

        instance: Optional[Performer] = self.get_instance_by_id(
            class_name=Performer,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую страну с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: PerformerBaseSerializer = PerformerBaseSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_performer: Performer = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_performer,
            serializer_class=PerformerDetailSerializer
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
