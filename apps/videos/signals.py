from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from django.db.models.base import ModelBase

from videos.models import (
    Video,
    VideoKeeper,
)


@receiver(signal=post_save, sender=Video)
def post_save_video(
    sender: ModelBase,
    instance: Video,
    created: bool,
    **kwargs
) -> None:
    """Signal for post save chat."""
    # Add owner to the keepers of the video

    if not VideoKeeper.objects.filter(
        video=instance,
        user=instance.owner
    ).exists():
        VideoKeeper.objects.create(
            video=instance,
            user=instance.owner
        )
