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
from rest_framework.decorators import action
from rest_framework import permissions

from abstracts.mixins import (
    DeletedRequestMixin,
    ModelInstanceMixin,
)
from abstracts.paginators import AbstractPageNumberPaginator
from abstracts.handlers import NoneDataHandler
from videos.models import Video, VideoKeeper
from videos.serializers import (
    VideoBaseModelSerializer,
    VideoListSerializer,
    VideoDetailSerializer,
)


class VideoViewSet(
    ModelInstanceMixin,
    NoneDataHandler,
    DeletedRequestMixin,
    ViewSet
):
    """VideoViewSet."""

    queryset: QuerySet[Video] = \
        Video.objects.all()
    serializer_class: VideoBaseModelSerializer = VideoBaseModelSerializer
    permission_classes: Tuple[Any] = (
        IsAuthenticated,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted().\
            select_related("owner")

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request for all videos."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=VideoListSerializer,
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
        """Handle GET-request with specified PK (ID)."""
        is_deleted: bool = request.data.get("is_deleted", False)
        if not is_deleted:
            is_deleted = kwargs.get("is_deleted", False)

        video: Optional[Video] = None
        if not is_deleted:
            video = self.get_queryset_instance_by_id(
                class_name=Video,
                queryset=self.get_queryset(),
                pk=pk
            )
        else:
            video = self.get_queryset_instance_by_id(
                class_name=Video,
                queryset=self.queryset.get_deleted(),
                pk=pk
            )

        response: Optional[DRF_Response] = self.get_none_response(
            object=video,
            message=f"Видео с PK {pk} не найдено или было удалено",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            response = self.get_drf_response(
                request=request,
                data=video,
                serializer_class=VideoDetailSerializer
            )
        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[str],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to create new Video."""
        serializer: VideoBaseModelSerializer = self.serializer_class(
            data=request.data
        )

        valid: bool = serializer.is_valid()

        if valid:
            request_owner_id: int = int(request.data["owner"])
            if request.user.id != request_owner_id:
                return DRF_Response(
                    data={
                        "response": "ID владельца не совпадают"
                    }
                )

            new_video: Video = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_video,
                serializer_class=VideoListSerializer
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

        instance: Optional[Video] = self.get_queryset_instance_by_id(
            class_name=Video,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такое видео с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: VideoBaseModelSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        updated_video: Video = serializer.save()

        return self.get_drf_response(
            request=request,
            data=updated_video,
            serializer_class=VideoListSerializer
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
        url_path="add",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def add_video(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle request to add Video."""
        video: Optional[Video] = self.get_queryset_instance_by_id(
            class_name=Video,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=video,
            message=f"Видео с PK {pk} не найдено или было удалено",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            if VideoKeeper.objects.filter(
                video=video,
                user=request.user
            ).exists():
                response = DRF_Response(
                    data={
                        "response": "У вас уже есть это видео"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                VideoKeeper.objects.create(
                    video=video,
                    user=request.user
                )
                response = DRF_Response(
                    data={
                        "response": "Видео успешно добавлено"
                    },
                    status=status.HTTP_200_OK
                )
        return response

    @action(
        methods=["get"],
        detail=True,
        url_path="remove",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def remove_video(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle request to add Video."""
        video: Optional[Video] = self.get_queryset_instance_by_id(
            class_name=Video,
            queryset=self.get_queryset(),
            pk=pk
        )
        response: Optional[DRF_Response] = self.get_none_response(
            object=video,
            message=f"Видео с PK {pk} не найдено или было удалено",
            status=status.HTTP_400_BAD_REQUEST
        )
        if not response:
            if not VideoKeeper.objects.filter(
                video=video,
                user=request.user
            ).exists():
                response = DRF_Response(
                    data={
                        "response": "У вас нет такого видео, чтобы удалить"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                found_video: VideoKeeper = VideoKeeper.objects.get(
                    video=video,
                    user=request.user
                )
                found_video.delete()

                response = DRF_Response(
                    data={
                        "response": "Видео успешно удалено"
                    },
                    status=status.HTTP_200_OK
                )
        return response

    @action(
        methods=["get"],
        detail=False,
        url_path="added_videos",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def get_added_user_videos(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to view all user's videos."""
        if request.user.datetime_deleted:
            return DRF_Response(
                data={"response": "Извините, ваш аккаунт удален"},
                status=status.HTTP_403_FORBIDDEN
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=request.user.added_videos.get_not_deleted(),
            serializer_class=VideoListSerializer,
            many=True,
            paginator=self.pagination_class()
        )

        return response

    @action(
        methods=["get"],
        detail=False,
        url_path="owned_videos",
        permission_classes=(
            permissions.IsAuthenticated,
        )
    )
    def get_owned_user_videos(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to view all user's videos."""
        if request.user.datetime_deleted:
            return DRF_Response(
                data={"response": "Извините, ваш аккаунт удален"},
                status=status.HTTP_403_FORBIDDEN
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset().filter(owner=request.user),
            serializer_class=VideoListSerializer,
            many=True,
            paginator=self.pagination_class()
        )

        return response
