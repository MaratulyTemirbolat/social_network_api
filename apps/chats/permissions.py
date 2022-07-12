from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request

from chats.models import (
    Chat,
)


class IsMemberOrAdmin(BasePermission):
    """IsOwner permission."""

    def has_permission(
        self,
        request: DRF_Request,
        view: Any
    ) -> bool:
        """Handle."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(
        self,
        request: DRF_Request,
        view: Any,
        obj: Chat
    ) -> bool:
        """Identify the owner."""
        return bool(
            (request.user and obj.members.get_not_deleted()
                .filter(id=request.user.id)
                .exists()) or
            (request.user and request.user.is_staff)
        )


class IsOwnerOrAdmin(BasePermission):
    """IsOwner permission."""

    def has_permission(
        self,
        request: DRF_Request,
        view: Any
    ) -> bool:
        """Handle."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(
        self,
        request: DRF_Request,
        view: Any,
        obj: Chat
    ) -> bool:
        """Identify the owner."""
        return bool(
            (request.user and obj.owner == request.user) or
            (request.user and request.user.is_staff)
        )


def get_chat_permission(
    request: DRF_Request,
    obj: Chat
) -> bool:
    """Identify the owner."""
    breakpoint()
    return bool(
        (request.user and obj.members.get_not_deleted()
            .filter(id=request.user.id)
            .exists()) or
        (request.user and request.user.is_staff)
    )
