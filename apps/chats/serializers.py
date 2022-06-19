from typing import (
    Tuple,
    Optional,
)
from datetime import datetime

from django.utils.text import slugify

from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SlugField,
    DateTimeField,
    CharField,
    BooleanField,
    SerializerMethodField,
)
from traitlets import default
from auths.models import CustomUser

from chats.models import (
    Chat,
    ChatMember,
)


class ChatMembersListSerailizer(ModelSerializer):
    """Serializer class between Chat and its members."""

    class Meta:
        """Class for serializer structure."""

        model: ChatMember = ChatMember
        fields: Tuple[str] = (
            "user",
            "chat_name",
        )


class ChatSingleSerializer(ModelSerializer):
    """Chat serializer for Single instance."""

    members: SerializerMethodField = SerializerMethodField(
        method_name="get_members"
    )

    class Meta:
        """Class for serializer structure."""

        model: Chat = Chat
        fields: Tuple[str] = (
            "id", "name", "slug",
            "is_group", "datetime_created",
            "photo_url", "is_deleted",
            "members",
        )

    def get_members(self, obj: Chat):  # noqa
        # qset = ChatMember.objects.filter(
        #     chat_id=obj.id
        # )
        qset = Chat.objects.get_not_deleted().prefetch_related(
            "members"
        )
        # breakpoint()
        return [ChatMembersSerailizer(m).data for m in qset]


class TrialModelChatSer(ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class ChatOwnerSerializer(ModelSerializer):
    class Meta:
        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            "id",
            "slug",
            "username",
        )


class ChatBaseSerializer(ModelSerializer):
    """Chat serializer by ModelSerializer class."""

    name: CharField = CharField()
    slug: SlugField = SlugField()
    is_group: BooleanField = BooleanField()
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


class ChatCreateSerializer(ChatBaseSerializer):
    """Chat serializer by ModelSerializer class."""

    pass
