from typing import (
    Tuple,
)

from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    EmailField,
    BooleanField,
    DateTimeField
)

from auths.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    """CustomUserSerializer."""

    id = IntegerField(read_only=True)
    email = EmailField(read_only=True)
    is_active = BooleanField(read_only=True)
    is_staff = BooleanField(read_only=True)
    date_joined = DateTimeField(read_only=True)
    datetime_created = DateTimeField(read_only=True)
    datetime_updated = DateTimeField(read_only=True)
    datetime_deleted = DateTimeField(read_only=True)

    class Meta:  # noqa
        model: CustomUser = CustomUser
        fields: Tuple[str] = (
            'id',
            'email',
            'is_active',
            'is_staff',
            'date_joined',
            'datetime_created',
            'datetime_updated',
            'datetime_deleted',
        )
