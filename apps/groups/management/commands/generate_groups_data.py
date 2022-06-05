import random
import names
from datetime import (
    date,
    datetime
)
from typing import (
    List,
    Sequence,
    Tuple,
    Any,
    Dict,
)
import radar

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify

from groups.models import (
    Group,
)


class Command(BaseCommand):
    """Custom command for filling up database.

    Generate Test data only for database.
    For each App you create another own Command
    """

    help = 'Custom command for filling up database.'

    __email_patterns: tuple = (
        'gmail.com', 'outlook.com', 'yahoo.com',
        'inbox.ru', 'inbox.ua', 'inbox.kz',
        'yandex.ru', 'yandex.ua', 'yandex.kz',
        'mail.ru', 'mail.ua', 'mail.kz',
    )

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:  # noqa
        super().__init__(args, kwargs)


    def handle(self, *args: tuple, **kwargs: dict) -> None:
        # Автоматически вызывается, когда вызывается generate_data файл
        """Handle data filling."""
        GEN_USER_COUNT = 150
        SUPERUSER_COUNT = 10

        start: datetime = datetime.now()
        # Получаем время в начале срабатывания кода, чтобы высчитать разницу

        self.__generate_users(gen_users=GEN_USER_COUNT)
        self.__generate_users(gen_users=SUPERUSER_COUNT, is_super_user=True)
        self.__generate_phones()
        self.__generate_friends()

        # Выдаем время генерации данных
        print(
            'Генерация данных составила: {} секунд'.format(
                (datetime.now()-start).total_seconds()
            )
        )
