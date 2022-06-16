from typing import (
    Tuple,
    Optional,
)

from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SlugField,
    DateTimeField,
    CharField,
    BooleanField,
    SerializerMethodField,
)

from chats.models import (
    Chat,
    ChatMember,
)


class ChatMembersSerailizer(ModelSerializer):
    """Serializer class between Chat and its members."""

    id: IntegerField = IntegerField(read_only=True)
    slug: SlugField = SlugField(read_only=True)
    username: CharField = CharField(read_only=True)

    class Meta:
        """Class for serializer structure."""

        model: ChatMember = ChatMember
        fields: Tuple[str] = (
            "id", "slug", "username",
        )


class ChatModelSerializer(ModelSerializer):
    """Chat serializer by ModelSerializer class."""

    id: IntegerField = IntegerField(read_only=True)
    name: CharField = CharField()
    slug: SlugField = SlugField(read_only=True)
    is_group: BooleanField = BooleanField(read_only=True)
    photo_url: SerializerMethodField = SerializerMethodField(
        method_name="get_photo_url",
    )
    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M"
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )
    members: ChatMembersSerailizer = ChatMembersSerailizer(
        many=True
    )

    class Meta:
        """Meta class which defines the logic."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id", "name", "slug",
            "is_group", "datetime_created",
            "photo_url", "is_deleted",
            "members",
        )
        # fields: str = "__all__"

    def get_photo_url(self, obj: Chat) -> Optional[str]:
        """Get full url of the photo."""
        if obj.photo:
            request = self.context.get("request")
            photo_url = obj.photo.url
            return request.build_absolute_uri(photo_url)
        return None

    def get_is_deleted(self, obj: Chat) -> bool:
        """Get is_deleted variable."""
        if obj.datetime_deleted:
            return True
        return False
