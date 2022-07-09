from typing import (
    Tuple,
)

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)

from music.models import (
    Playlist,
    Music,
    Performer,
)
from abstracts.mixins import AbstractDateTimeSerializerMixin


class PerformerBaseSerializer(AbstractDateTimeSerializerMixin, ModelSerializer):
    """PerformerBaseSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted

    class Meta:
        """Customization of the Serializer."""

        model: Performer = Performer
        fields: Tuple[str] = (
            "id",
            "username",
            "slug",
            "datetime_created",
            "is_deleted",
        )


# Music Serializers
class MusicBaseSerializer(AbstractDateTimeSerializerMixin, ModelSerializer):
    """MusicBaseSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted

    class Meta:
        """Customization of the Serializer."""

        model: Music = Music
        fields: Tuple[str] = (
            "id",
            "performers",
            "datetime_created",
            "is_deleted",
        )


class MusicDetailSerializer(MusicBaseSerializer):
    """MusicDetailSerializer."""

    performers: PerformerBaseSerializer = PerformerBaseSerializer(
        many=True
    )


# Playlist Serializers
class PlaylistBaseSerializer(AbstractDateTimeSerializerMixin, ModelSerializer):
    """PlaylistBaseSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: Playlist = Playlist
        fields: Tuple[str] = (
            "id",
            "name",
            "photo",
            "datetime_created",
            "is_deleted",
        )


class PlaylistDetailSerializer(PlaylistBaseSerializer):
    """PlaylistDetailSerializer."""

    songs: MusicDetailSerializer = MusicDetailSerializer(
        source="playlist_songs",
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Playlist = Playlist
        fields: Tuple[str] = (
            "id",
            "name",
            "photo",
            "datetime_created",
            "is_deleted",
            "songs",
        )
