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
from auths.serializers import CustomUserShortSerializer


# Performer Serializers
class PerformerBaseSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
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
class MusicBaseSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
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
            "playlist",
            "datetime_created",
            "is_deleted",
        )


class MusicListSerializer(MusicBaseSerializer):
    """MusicListSerializer."""

    performers: PerformerBaseSerializer = PerformerBaseSerializer(
        many=True
    )


class MusicDetailSerializer(MusicListSerializer):
    """MusicDetailSerializer."""

    users: CustomUserShortSerializer = CustomUserShortSerializer(
        many=True
    )
    listeners_number: SerializerMethodField = SerializerMethodField(
        method_name="get_listeners_number"
    )

    class Meta:
        """Customization of the Serializer."""

        model: Music = Music
        fields: Tuple[str] = (
            "id",
            "music",
            "performers",
            "playlist",
            "datetime_created",
            "is_deleted",
            "users",
            "listeners_number",
        )

    def get_listeners_number(self, obj: Music) -> int:
        return obj.users.count()


# Playlist Serializers
class PlaylistBaseSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
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

    songs: MusicListSerializer = MusicListSerializer(
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

    performer_songs: MusicListSerializer = MusicListSerializer(
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
