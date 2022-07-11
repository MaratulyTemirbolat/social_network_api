from typing import Optional

from rest_framework.response import Response as DRF_Response
from rest_framework import status

from auths.models import (
    CustomUser,
    YOU_BLOCKED_STATE,
    YOU_ARE_BLOCKED_STATE,
    ALREADY_FRIENDS_STATE,
    ALREADY_REQUEST_SENT_STATE,
)


def is_superuser_authenticated(user: CustomUser) -> bool:
    """Handle if superuser is authenticated or not."""
    if user.is_authenticated:
        if user.is_superuser:
            return True
    return False


def get_friends_drf_response(
    friends_state: Optional[int],
    targer_username: str
) -> DRF_Response:
    """Get DRF_Response on Friends state."""
    if not friends_state:
        return DRF_Response(
            data={
                "response": f"Запрос к {targer_username} успешно отправле"
            },
            status=status.HTTP_201_CREATED
        )

    message: str
    if friends_state == YOU_BLOCKED_STATE:
        message = f"Разблокируйте пользователя {targer_username}"
    elif friends_state == YOU_ARE_BLOCKED_STATE:
        message = f"Вы заблокированы пользователем {targer_username}"
    elif friends_state == ALREADY_FRIENDS_STATE:
        message = f"Вы уже друзья с пользователем {targer_username}"
    else:
        message = "Ваш запрос на добавление в друзья уже отправлен"
    return DRF_Response(
        data={
            "response": message
        },
        status=status.HTTP_400_BAD_REQUEST
    )
