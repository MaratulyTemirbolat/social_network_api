from typing import (
    Tuple,
)

from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    EmailField,
    BooleanField,
    DateTimeField,
    CharField,
    ReadOnlyField,
    SerializerMethodField,
    SlugField,
    HiddenField,
    CurrentUserDefault,
)

from auths.models import (
    CustomUser,
    Friends,
    Phone,
)
from abstracts.mixins import AbstractDateTimeSerializerMixin


# Phone Serializers
class PhoneBaseSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """PhoneSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    owner: HiddenField = HiddenField(
        default=CurrentUserDefault()
    )

    class Meta:
        """Phone Serializer's setting."""

        model: Phone = Phone
        fields: Tuple[str] = (
            "id",
            "phone",
            "owner",
            "is_deleted",
            "datetime_created",
        )


# Friend Serializers
class FriendBaseSerializer(ModelSerializer):
    """FrienBaseSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Friends = Friends
        fields: Tuple[str] = (
            "to_user",
            "is_blocked",
        )


# CustomUser Serializers
class CustomUserBaseSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """CustomUserBaseSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    slug: SlugField = SlugField(read_only=True)
    last_login: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        read_only=True
    )
    is_active: BooleanField = BooleanField(
        read_only=True
    )
    is_staff: BooleanField = BooleanField(
        read_only=True
    )
    is_superuser: BooleanField = BooleanField(
        read_only=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            "id",
            "username",
            "slug",
            "birthday",
            "email",
            "first_name",
            "last_name",
            "last_login",
            "is_active",
            "is_staff",
            "is_deleted",
            "datetime_created",
            "is_superuser",
        )


class CustomUserDetailSerializer(CustomUserBaseSerializer):
    """CustomUserDetailSerializer."""

    phones: PhoneBaseSerializer = PhoneBaseSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            "id",
            "username",
            "slug",
            "birthday",
            "email",
            "first_name",
            "last_name",
            "last_login",
            "is_active",
            "is_staff",
            "is_deleted",
            "datetime_created",
            "phones",
        )


class FriendsSerializer(ModelSerializer):
    """FriendsSerializer."""

    id: ReadOnlyField = ReadOnlyField()
    username: ReadOnlyField = ReadOnlyField()
    is_blocked: BooleanField = BooleanField(
        read_only=True
    )

    class Meta:
        """Friends Serializer's setting."""

        model: Friends = Friends
        fields: Tuple[str] = (
            "id",
            "username",
            "is_blocked",
        )


class CustomUserSerializer(ModelSerializer):
    """CustomUserSerializer."""

    id = IntegerField(read_only=True)
    email = EmailField(read_only=True)
    first_name = CharField(read_only=True)
    last_name = CharField(read_only=True)
    is_active = BooleanField(read_only=True)
    is_staff = BooleanField(read_only=True)
    last_login = DateTimeField(read_only=True)
    datetime_created = DateTimeField(read_only=True)
    datetime_updated = DateTimeField(read_only=True)
    datetime_deleted = DateTimeField(read_only=True)
    friendss = FriendsSerializer(
        many=True
    )

    class Meta:
        """CustomUser Serializer's setting."""

        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "last_login",
            "datetime_created",
            "datetime_updated",
            "datetime_deleted",
            "friendss",
        )


class CustomUserShortSerializer(ModelSerializer):
    """CustomUserShortSerializer."""

    class Meta:
        """Customizing own serializer."""

        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            "id",
            "slug",
            "username",
            "last_login",
        )


# Phone Serializer that is related to the CustomUser
class PhoneDetailSerializer(PhoneBaseSerializer):
    """PhoneDetailSerializer."""

    owner: CustomUserShortSerializer = CustomUserShortSerializer()
