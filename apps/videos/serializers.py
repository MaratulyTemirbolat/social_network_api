from typing import Tuple

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)

from auths.serializers import CustomUserShortSerializer
from abstracts.mixins import AbstractDateTimeSerializerMixin
from videos.models import Video


# Video model Serializers
class VideoBaseModelSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """VideoBaseSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: Video = Video
        fields: Tuple[str] = (
            "id",
            "name",
            "video_file",
            "owner",
            "is_deleted",
            "datetime_created",
        )


class VideoListSerializer(VideoBaseModelSerializer):
    """VideoDetailSerializer."""

    owner: CustomUserShortSerializer = CustomUserShortSerializer()


class VideoDetailSerializer(VideoListSerializer):
    """VideoDetailSerializer."""

    keepers: CustomUserShortSerializer = CustomUserShortSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Video = Video
        fields: Tuple[str] = (
            "id",
            "name",
            "video_file",
            "owner",
            "keepers",
            "is_deleted",
            "datetime_created",
        )
