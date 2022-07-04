"""Serializers for complains app."""

from typing import Tuple
from datetime import datetime

from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    DateTimeField,
    SlugField,
)

from complains.models import (
    ComplainReason,
    ComplainNews,
)
from auths.serializers import CustomUserShortSerializer


class ComplainReasonSerializer(ModelSerializer):
    """ComplainReasonModelSerializer."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )
    slug: SlugField = SlugField(read_only=True)

    class Meta:
        """Customization of the class."""

        model: ComplainReason = ComplainReason
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
        )

    def get_is_deleted(self, obj: ComplainReason) -> bool:
        """Resolution of is_deleted variable."""
        if obj.datetime_deleted:
            return True
        return False


# Реализовать
class ComplainNewsBaseSerializer(ModelSerializer):
    """ComplainNewsSerializer."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )

    class Meta:
        """Customization of the class."""

        model: ComplainNews = ComplainNews
        fields: Tuple[str] = (
            "id",
            "content",
            "datetime_created",
            "is_deleted",
            "news",
            "reason",
            "owner",
        )

    def get_is_deleted(self, obj: ComplainReason) -> bool:
        """Resolution of is_deleted variable."""
        if obj.datetime_deleted:
            return True
        return False


class ComplainNewsDetailSerializer(ComplainNewsBaseSerializer):
    """ComplainNewsDetailSerializer."""

    owner: CustomUserShortSerializer = CustomUserShortSerializer()
    reason: ComplainReasonSerializer = ComplainReasonSerializer()
