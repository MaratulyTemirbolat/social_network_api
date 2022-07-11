from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request

from auths.models import CustomUser


class IsOwnerOrAdmin(BasePermission):
    """IsOwner permission."""

    def has_object_permission(
        self,
        request: DRF_Request,
        view: Any,
        obj: CustomUser
    ) -> bool:
        """Identify the owner."""
        return bool(
            (request.user and request.user == obj) or
            (request.user and request.user.is_staff)
        )
