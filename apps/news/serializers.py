from typing import Tuple

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    SlugField,
)

from abstracts.mixins import (
    AbstractDateTimeSerializerMixin,
)
from news.models import (
    Tag,
    News,
    Category,
)


# Tag Serializers
class TagBaseModelSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """TagBaseModelSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    slug: SlugField = SlugField(read_only=True)

    class Meta:
        """Customization of the Serializer."""

        model: Tag = Tag
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
        )


# News Serializers
class NewsBaseSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer
):
    """NewsBaseSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: News = News
        fields: Tuple[str] = (
            "id",
            "title",
            "photo",
            "group",
            "author",
            "is_deleted",
            "datetime_created",
        )


class NewsDetailSerializer(NewsBaseSerializer):
    """NewsDetailSerializer."""

    likes_number: SerializerMethodField = SerializerMethodField(
        method_name="get_likes_number"
    )

    class Meta:
        """Customization of the Serializer."""

        model: News = News
        fields: Tuple[str] = (
            "id",
            "title",
            "photo",
            "group",
            "author",
            "likes_number",
            "is_deleted",
            "datetime_created",
        )

    def get_likes_number(self, obj: News):
        """View number of user likes."""
        return obj.liked_users.count()


# Tag Detail Serializer That is related to the News
class TagDetailSerializer(TagBaseModelSerializer):
    """TagDetailSerializer."""

    news: NewsBaseSerializer = NewsBaseSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Tag = Tag
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
            "news",
        )


# Category Serializers
class CategoryBaseModelSerializer(
    AbstractDateTimeSerializerMixin,
    ModelSerializer,
):
    """CategoryBaseModelSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializerMixin.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializerMixin.datetime_created
    slug: SlugField = SlugField(read_only=True)

    class Meta:
        """Customization of the Serializer."""

        model: Category = Category
        fields: Tuple[str] = (
            "id",
            "title",
            "slug",
            "datetime_created",
            "is_deleted",
        )


class CategoryDetailSerializer(CategoryBaseModelSerializer):
    """CategoryDetailSerializer."""

    news: NewsBaseSerializer = NewsBaseSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Category = Category
        fields: Tuple[str] = (
            "id",
            "title",
            "slug",
            "datetime_created",
            "is_deleted",
            "news",
        )
