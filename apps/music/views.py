from typing import (
    List,
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
    MusicBaseSerializer,
    PlaylistBaseSerializer,
    PlaylistDetailSerializer,
    PerformerBaseSerializer,
    PerformerDetailSerializer,
    MusicListSerializer,
    MusicDetailSerializer,
)
from music.tools import is_music_file
from abstracts.handlers import NoneDataHandler
from abstracts.paginators import AbstractPageNumberPaginator
from abstracts.models import AbstractDateTimeQuerySet
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


class MusicViewSet(
    NoneDataHandler,
    ModelInstanceMixin,
    DeletedRequestMixin,
    ViewSet
):
    """MusicViewSet."""

    queryset: QuerySet[Music] = \
        Music.objects.all()
    serializer_class: MusicBaseSerializer = MusicBaseSerializer
    permission_classes: Tuple[Any] = (
        IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted().select_related(
            "playlist"
        ).prefetch_related("performers")

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to get all music."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=MusicListSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    # КАК сделать Пагинацию на пользователей при получении песни
    def retrieve(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with specified ID."""
        music: Optional[Music] = self.get_instance_by_id(
            class_name=Music,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=music,
            message=f"Данной песни c ID {pk} не существует или она удалена",
            status=status.HTTP_404_NOT_FOUND
        )
        if not response:
            response = self.get_drf_response(
                request=request,
                data=music,
                serializer_class=MusicDetailSerializer
            )
        return response

    # Протестить, чтобы файл можно было в JSON отправлять
    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new Music."""
        correct_file: bool = is_music_file(request.data.get("music", ""))

        is_playlist_exist: bool = Playlist.objects.filter(
            id=request.data.get("playlist", -1)
        ).exists()

        existed_performers: int = \
            Performer.objects.get_not_deleted().\
            filter(id__in=request.data.get('performers', [])).count()

        error_message: str = ""
        if not correct_file:
            error_message = "Файл 'music' не того типа или не предоставлен"
        elif not is_playlist_exist:
            error_message = "Поле 'playlist' должно быть корректным"
        elif len(request.data.get("performers", [])) != existed_performers:
            error_message = "Не все указанные исполнители существуют"

        if error_message:
            return DRF_Response(
                data={
                    "response": "Объект не создан",
                    "message": error_message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer: MusicBaseSerializer = self.serializer_class(
            data=request.data
        )

        valid: bool = serializer.is_valid()
        if valid:
            new_music: Music = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_music,
                serializer_class=MusicDetailSerializer
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

        instance: Optional[Music] = self.get_instance_by_id(
            class_name=Music,
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую страну с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: MusicBaseSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_music: Music = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_music,
            serializer_class=MusicDetailSerializer
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

    @action(
        methods=["get"],
        detail=True,
        url_path="add_music",
        permission_classes=(
            IsAuthenticated,
        )
    )
    def add_music(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to be added."""
        music: Optional[Music] = self.get_instance_by_id(
            Music,
            pk=pk
        )
        if not music:
            return DRF_Response(
                {"response": "Данной песни не существует или она удалена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        error: bool = False
        error_message: str = ""
        if not request.user.is_active:
            error = True
            error_message = "Ваш аккаунт был удален!"
        elif music.users.filter(id=request.user.id).exists():
            error = True
            error_message = "У вас уже есть такая песня"

        if error:
            return DRF_Response(
                data={
                    "response": "Песня не добавлена",
                    "message": error_message
                },
                status=status.HTTP_403_FORBIDDEN
            )

        music.users.add(request.user)

        return DRF_Response(
            data={
                "response": "Песня успешно добавлена"
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=["get"],
        detail=True,
        url_path="remove_music",
        permission_classes=(
            IsAuthenticated,
        )
    )
    def remove_music(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to be added."""
        music: Optional[Music] = self.get_instance_by_id(
            Music,
            pk=pk
        )
        if not music:
            return DRF_Response(
                {"response": "Данной песни не существует или она удалена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        error: bool = False
        error_message: str = ""
        if not request.user.is_active:
            error = True
            error_message = "Ваш аккаунт был удален!"
        elif not music.users.filter(id=request.user.id).exists():
            error = True
            error_message = "У вас нет такой песни"

        if error:
            return DRF_Response(
                data={
                    "response": "Песня не удалена",
                    "message": error_message
                },
                status=status.HTTP_403_FORBIDDEN
            )

        music.users.remove(request.user)

        return DRF_Response(
            data={
                "response": "Песня успешно удалена"
            },
            status=status.HTTP_200_OK
        )
