
from logging import (
    getLogger,
    Logger,
)

from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save,
    post_delete,
    pre_delete,
)
from django.db.models.base import ModelBase
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from auths.models import (
    CustomUser,
)

logger: Logger = getLogger('wagtail.core')


@receiver(
    signal=post_save,
    sender=CustomUser
)
def post_save_anime(
    sender: ModelBase,
    instance: CustomUser,
    created: bool,
    **kwargs: dict
) -> None:
    """Signal post-save Anime."""
    my_dict: dict = {'username': instance.username}
    html_template: str = 'register_email.html'
    html_message: str = render_to_string(
        template_name=html_template,
        context=my_dict
    )
    subject: str = 'Welcome to TEMIRBOLAT social network'
    email_from: str = settings.EMAIL_HOST_USER
    recipient_list = [instance.email]
    message: EmailMessage = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=email_from,
        to=recipient_list
    )
    message.content_subtype = 'html'
    message.send()
