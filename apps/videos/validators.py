from typing import (
    Any,
    Union,
)

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile


VIDEO_FILE_FORMATS = ("video/mp4",)


def video_format_validator(
    file: Union[TemporaryUploadedFile, Any]
) -> None:
    """Validate the file to be video."""
    if not isinstance(file, TemporaryUploadedFile):
        raise ValidationError(
            message="Ваш файл должен быть по типу mp4 (video)",
            code="video_file_type_error"
        )
    else:
        if file.content_type not in VIDEO_FILE_FORMATS:
            raise ValidationError(
                message="Расширение файла не по типу видео",
                code="video_file_type_error"
            )
