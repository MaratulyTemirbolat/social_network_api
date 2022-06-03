# from typing import (
#     Tuple,
# )

from django.forms import CharField
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

    # id = IntegerField(read_only=True)
    # email = EmailField(read_only=True)
    # first_name = CharField(read_only=True)
    # last_name = CharField(read_only=True)
    # is_active = BooleanField(read_only=True)
    # is_staff = BooleanField(read_only=True)
    # date_joined = DateTimeField(read_only=True)
    # datetime_created = DateTimeField(read_only=True)
    # datetime_updated = DateTimeField(read_only=True)
    # datetime_deleted = DateTimeField(read_only=True)

    class Meta:  # noqa
        model: CustomUser = CustomUser
        fields: str = '__all__'
