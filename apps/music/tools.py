from typing import (
    Union,
    Any,
)

from django.core.files.uploadedfile import TemporaryUploadedFile


MUSIC_FILE_TYPES = ('audio/mpeg',)


def is_music_file(
    file: Union[TemporaryUploadedFile, Any]
) -> bool:
    """Check the Music file type."""
    if isinstance(file, TemporaryUploadedFile):
        if file.content_type in MUSIC_FILE_TYPES:
            return True
    return False
