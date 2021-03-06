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
    HiddenField,
    CurrentUserDefault,
)
from traitlets import default

from auths.models import CustomUser
from auths.serializers import CustomUserShortSerializer
from chats.models import (
    Chat,
    ChatMember,
    Message,
)
from abstracts.mixins import AbstractDateTimeSerializerMixin


# ChatMemberListSerializers
class ChatMembersListSerailizer(ModelSerializer):
    """Serializer class between Chat and its members."""

    class Meta:
        """Class for serializer structure."""

        model: ChatMember = ChatMember
        fields: Tuple[str] = (
            "user",
            "chat_name",
        )


class ChatMemberBaseModelSerializer(ModelSerializer):
    """ChatMemberBaseModelSerializer."""

    class Meta:
        """Customization."""

        model: ChatMember = ChatMember
        fields: str = "__all__"


# Message Serializers
class MessageBaseModelSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """MessageBaseModelSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    owner: HiddenField = HiddenField(
        default=CurrentUserDefault()
    )

    class Meta:
        """Customization of the Serializer."""

        model: Message = Message
        fields: Tuple[str] = (
            "id",
            "content",
            "owner",
            "is_deleted",
            "datetime_created",
            "chat",
        )


class MessageListSerializer(MessageBaseModelSerializer):
    """MessageListSerializer."""

    owner: CustomUserShortSerializer = CustomUserShortSerializer()


# Chat serializers
class ChatBaseModelSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """ChatBaseModelSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    owner: HiddenField = HiddenField(default=CurrentUserDefault())

    class Meta:
        """Customization of the Serializer."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "is_group",
            "photo",
            "owner",
            "is_deleted",
            "datetime_created",
        )


class ChatListSerializer(ChatBaseModelSerializer):
    """ChatDetailSerializer."""

    owner: CustomUserShortSerializer = CustomUserShortSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "is_group",
            "photo",
            "owner",
            "is_deleted",
            "datetime_created",
        )


class ChatDetailSerializer(ChatListSerializer):
    """ChatDetailSerializer."""

    owner: CustomUserShortSerializer = CustomUserShortSerializer()
    members: ChatMembersListSerailizer = ChatMembersListSerailizer(
        source="chatmember_set",
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "is_group",
            "photo",
            "owner",
            "is_deleted",
            "datetime_created",
            "members",
        )


class ChatUpdateSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """ChatBaseModelSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "is_group",
            "photo",
            "owner",
            "is_deleted",
            "datetime_created",
        )


#
class MessageModelSerializer(ModelSerializer):
    """MessageModelSerializer."""

    is_edited: SerializerMethodField = SerializerMethodField(
        method_name="get_is_edited"
    )
    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
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
