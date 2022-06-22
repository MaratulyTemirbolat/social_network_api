from typing import (
    Tuple,
    Optional,
)
from datetime import (
    datetime,
    timedelta,
)

from rest_framework.serializers import (
    ModelSerializer,
    SlugField,
    DateTimeField,
    CharField,
    BooleanField,
    SerializerMethodField,
)

from auths.models import CustomUser
from auths.serializers import CustomUserShortSerializer
from chats.models import (
    Chat,
    ChatMember,
    Message,
)


class MessageModelSerializer(ModelSerializer):
    """MessageModelSerializer."""

    is_edited: SerializerMethodField = SerializerMethodField(
        method_name="get_is_edited"
    )
    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M:%s",
        read_only=True
    )
    owner: CustomUserShortSerializer = CustomUserShortSerializer()

    class Meta:
        """Customization of the class."""

        model: Message = Message
        fields: Tuple[str] = (
            "id",
            "datetime_created",
            "content",
            "owner",
            "is_edited",
        )

    def get_is_edited(self, obj: Message) -> bool:
        """Get is_edited."""
        ONE_SECOND = 1.0
        difference: timedelta = obj.datetime_updated - obj.datetime_created
        if difference.total_seconds() > ONE_SECOND:
            return True
        return False


class ChatMembersListSerailizer(ModelSerializer):
    """Serializer class between Chat and its members."""

    class Meta:
        """Class for serializer structure."""

        model: ChatMember = ChatMember
        fields: Tuple[str] = (
            "user",
            "chat_name",
        )


class ChatOwnerSerializer(ModelSerializer):
    """ChatOnwerSerializer."""

    class Meta:
        """Customization of the ChatOwnerSerializer model."""

        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            "id",
            "slug",
            "username",
        )


class ChatBaseSerializer(ModelSerializer):
    """Chat serializer by ModelSerializer class."""

    name: CharField = CharField()
    slug: SlugField = SlugField(read_only=True)
    is_group: BooleanField = BooleanField(read_only=True)
    # photo_url: SerializerMethodField = SerializerMethodField(
    #     method_name="get_photo_url",
    # )
    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )

    class Meta:
        """Meta class which defines the logic."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "is_group",
            "datetime_created",
            "photo",
            # "photo_url",
            "is_deleted",
            "owner",
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


class ChatViewSerializer(ChatBaseSerializer):
    """Chat serializer by ModelSerializer class."""

    members: ChatMembersListSerailizer = ChatMembersListSerailizer(
        source="chatmember_set",
        many=True,
        required=False,
        allow_null=True
    )
    owner: ChatOwnerSerializer = ChatOwnerSerializer()


class ChatViewSingleSerializer(ChatViewSerializer):
    """ChatViewSingleSerializer."""

    messages: MessageModelSerializer = MessageModelSerializer(
        # source="messages",
        many=True
    )

    class Meta:
        """Meta class which defines the logic."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "is_group",
            "datetime_created",
            "photo",
            "is_deleted",
            "owner",
            "members",
            "messages",
        )


class ChatCreateSerializer(ChatBaseSerializer):
    """Chat serializer by ModelSerializer class."""

    pass
