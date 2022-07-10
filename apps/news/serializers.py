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
from auths.serializers import CustomUserShortSerializer
from news.models import (
    Tag,
    News,
    Category,
)
from groups.serializers import GroupBaseSerializer


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
            "category",
            "is_deleted",
            "datetime_created",
        )


class NewsListSerializer(NewsBaseSerializer):
    """NewsListSerializer."""

    group: GroupBaseSerializer = GroupBaseSerializer()
    author: CustomUserShortSerializer = CustomUserShortSerializer()
    category: CategoryBaseModelSerializer = CategoryBaseModelSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: News = News
        fields: Tuple[str] = (
            "id",
            "title",
            "photo",
            "content",
            "group",
            "author",
            "category",
            "is_deleted",
            "datetime_created",
        )


class NewsCreateSerializer(NewsBaseSerializer):
    """NewsListSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: News = News
        fields: Tuple[str] = (
            "id",
            "title",
            "photo",
            "content",
            "group",
            "author",
            "category",
            "tags",
            "is_deleted",
            "datetime_created",
        )


class NewsDetailSerializer(NewsListSerializer):
    """NewsDetailSerializer."""

    likes_number: SerializerMethodField = SerializerMethodField(
        method_name="get_likes_number"
    )
    tags: TagBaseModelSerializer = TagBaseModelSerializer(
        many=True
    )
    liked_users: CustomUserShortSerializer = CustomUserShortSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: News = News
        fields: Tuple[str] = (
            "id",
            "title",
            "photo",
            "content",
            "group",
            "author",
            "category",
            "is_deleted",
            "datetime_created",
            "likes_number",
            "liked_users",
            "tags",
        )

    def get_likes_number(self, obj: News):
        """View number of user likes."""
        return obj.liked_users.count()


class NewsUpdateSerializer(NewsBaseSerializer):
    """NewsUpdateSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: News = News
        fields: Tuple[str] = (
            "id",
            "title",
            "photo",
            "content",
            "group",
            "author",
            "category",
            "tags",
            "is_deleted",
            "datetime_created",
        )


# Tag Detail Serializer That is related to the NewsSerializer
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


# Categor Detail Serializer That is related to NewsSerializer
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
