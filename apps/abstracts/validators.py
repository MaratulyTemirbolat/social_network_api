"""General Abstract custom validators."""
import pytz
from typing import (
    Optional,
    Dict,
)
from datetime import datetime

from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import APIException

from django.core.exceptions import ValidationError
from django.utils.encoding import force_str


class APIValidator(APIException):
    """General-purpose validator for API."""

    status_code: Optional[str] = None

    def __init__(
        self,
        field: str,
        detail: Optional[Dict[str, str]] = None,
        status_code: Optional[str] = None
    ) -> None:
        """Initialize parameters."""
        if status_code == '500':
            self.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        elif status_code == '404':
            self.status_code = HTTP_404_NOT_FOUND
        elif status_code == '403':
            self.status_code = HTTP_403_FORBIDDEN
        elif status_code == '400':
            self.status_code = HTTP_400_BAD_REQUEST
        else:
            raise ValidationError(
                "Status code is unknown"
            )
        if detail:
            self.detail = {
                field: force_str(detail)
            }
        else:
            self.detail = {
                "error": force_str("Server is down")
            }


class AbstractValidator:
    """General-purpose validator."""

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize."""
        pass  # ПОПРОСИТЬ

    def validate_release_date(self, release_date: datetime) -> None:
        """Validate ReleaseDate field from Anime."""
        if hasattr(self, 'id'):
            return None

        utc = pytz.UTC
        utc_now: datetime = utc.localize(
            datetime.now()
        )
        if release_date < utc_now:
            raise ValidationError(
                'Запрещено загружать Аниме с прошедшей датой релиза'
            )
