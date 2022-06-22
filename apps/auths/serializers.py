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
    SlugField,
    Serializer,
)

from auths.models import (
    CustomUser,
    Friends,
    Phone,
)


class NewPhoneSerializer(Serializer):
    """NewPhoneSerializer."""

    pass


class PhoneSerializer(ModelSerializer):
    """PhoneSerializer."""

    class Meta:
        """Phone Serializer's setting."""

        model: Phone = Phone
        fields: Tuple[str] = (
            "id",
            "phone",
            "owner",
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
