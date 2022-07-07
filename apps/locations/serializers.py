from typing import (
    Tuple,
)
from datetime import datetime

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    SlugField,
)

from locations.models import (
    Country,
    City,
)


class CityBaseModelSerializer(ModelSerializer):
    """CitryModelSerializer."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )

    class Meta:
        """Customization of serializer."""

        model: City = City
        exclude: Tuple[str] = (
            "datetime_updated",
            "datetime_deleted",
        )

    def get_is_deleted(self, obj: Country) -> bool:
        """Get if object deleted or not."""
        if obj.datetime_deleted:
            return True
        return False


class CityCountrySerializer(CityBaseModelSerializer):
    """CityCountrySerializer."""

    class Meta:
        """Customization of serializer."""

        model: City = City
        exclude: Tuple[str] = (
            "datetime_updated",
            "datetime_deleted",
            "country",
        )


# Country Serializers
class CountryBaseModelSerializer(ModelSerializer):
    """CountryModelSerializer."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        default=datetime.now(),
        read_only=True
    )
    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )
    slug: SlugField = SlugField(
        read_only=True
    )

    class Meta:
        """Customization of serializer."""

        model: Country = Country
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
        )

    def get_is_deleted(self, obj: Country) -> bool:
        """Get if object deleted or not."""
        if obj.datetime_deleted:
            return True
        return False


class CountryDetailModelSerializer(CountryBaseModelSerializer):
    """CountryDetailModelSerializer."""

    cities: CityCountrySerializer = CityCountrySerializer(
        source="attached_cities",
        many=True
    )

    class Meta:
        """Customization of serializer."""

        model: Country = Country
        fields: Tuple[str] = (
            "id",
            "name",
            "slug",
            "datetime_created",
            "is_deleted",
            "cities",
        )


# City Serializer related to Country
class CityDetailedSerializer(CityBaseModelSerializer):
    """CityDetailedSerializer."""

    country: CountryBaseModelSerializer = CountryBaseModelSerializer()
