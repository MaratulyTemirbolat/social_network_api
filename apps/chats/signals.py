from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from django.db.models.base import ModelBase

from chats.models import (
    Chat,
    ChatMember,
)


@receiver(signal=post_save, sender=Chat)
def post_save_chat(
    sender: ModelBase,
    instance: Chat,
    created: bool,
    **kwargs
) -> None:
    """Signal for post save chat."""
    # Add owner to the created by him group

    ChatMember.objects.get_or_create(
        chat_id=instance.id,
        user_id=instance.owner.id,
        chat_name=instance.owner.slug
    )
