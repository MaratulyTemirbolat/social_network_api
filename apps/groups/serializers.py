from typing import Tuple
from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    SerializerMethodField,
    SlugField,
)

from groups.models import (
    Group,
)


class GroupBaseSerializer(ModelSerializer):
    """GroupSerializer."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )
    slug: SlugField = SlugField()

    class Meta:
        """Customizing own serializer."""

        model: Group = Group
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
        )

    def get_is_deleted(self, obj: Group) -> bool:
        """Resolution of is_deleted variable."""
        if obj.datetime_deleted:
            return True
        return False


class GroupDetailSerializer(GroupBaseSerializer):
    """GroupDetailSerializer."""

    class Meta:
        """Customizing own serializer."""

        model: Group = Group
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
            "followers",
            "members_rights",
        )
