from typing import (
    Tuple,
)

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    SlugField,
)

from music.models import (
    Playlist,
    Music,
    Performer,
)
from abstracts.mixins import AbstractDateTimeSerializerMixin


# Performer Serializers
class PerformerBaseSerializer(AbstractDateTimeSerializerMixin, ModelSerializer):
    """PerformerBaseSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    slug: SlugField = SlugField(read_only=True)

    class Meta:
        """Customization of the Serializer."""

        model: Performer = Performer
        fields: Tuple[str] = (
            "id",
            "username",
            "slug",
            "name",
            "surname",
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
            "music",
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


# Performer Serializers with MusicRequirements to be first
class PerformerDetailSerializer(PerformerBaseSerializer):
    """PerformerDetailSerializer for detail view."""

    performer_songs: MusicDetailSerializer = MusicDetailSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Performer = Performer
        fields: Tuple[str] = (
            "id",
            "username",
            "slug",
            "name",
            "surname",
            "datetime_created",
            "is_deleted",
            "performer_songs",
        )
