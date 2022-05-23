from typing import (
    List,
)

from django.core.mail import send_mail
from django.conf import settings


def send_email(subject: str, text: str, receiver_emails: List[str]) -> None:  # noqa
    try:
        send_mail(
            subject=subject,
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=receiver_emails
        )
    except Exception as e:
        print("Email error:", e)
