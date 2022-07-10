from typing import Tuple

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)

from abstracts.mixins import AbstractDateTimeSerializerMixin
from videos.models import Video


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
        fields: str = "__str__"
