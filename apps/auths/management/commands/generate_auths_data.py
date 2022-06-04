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

from auths.models import (
    CustomUser,
    Phone,
    Friends,
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

    def __generate_users(
        self,
        gen_users: int = 0,
        is_super_user: bool = False
    ) -> None:
        def get_username(
            first_name: str,
            last_name: str,
            first_name_len: int,
            last_name_len: int
        ) -> str:
            short_first_name: str = first_name[:first_name_len]
            short_last_name: str = last_name[:last_name_len]
            return f'{short_first_name}_{short_last_name}'

        def get_email(first_name: str, last_name: str) -> str:
            email_end: str = random.choice(self.__email_patterns)
            return f'{first_name}_{last_name}@{email_end}'

        def generate_password() -> str:
            PASSWORD_PATTERN = "temirbolatm2001"
            return make_password(PASSWORD_PATTERN)

        def get_random_date() -> date:
            start_date: date = date(year=1950, month=1, day=1)
            end_date: date = date(year=2001, month=1, day=31)
            return radar.random_date(start=start_date, stop=end_date)

        model_users: List[CustomUser] = []

        _: int
        for _ in range(gen_users):
            first_name_len: int = random.randint(1, 6)
            last_name_len: int = random.randint(1, 6)
            first_name: str = names.get_first_name()
            last_name: str = names.get_last_name()
            username: str = get_username(
                first_name=first_name.lower(),
                last_name=last_name.lower(),
                first_name_len=first_name_len,
                last_name_len=last_name_len
            )
            email: str = get_email(
                first_name=first_name.lower(),
                last_name=last_name.lower()
            )
            birthday: date = get_random_date()
            password: str = generate_password()
            cur_user: dict = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'username': username,
                'birthday': birthday,
                'slug': slugify(username)
            }
            if is_super_user:
                model_users.append(
                    CustomUser(
                        is_staff=True,
                        is_superuser=True,
                        **cur_user
                    )
                )
            else:
                model_users.append(
                    CustomUser(
                        **cur_user
                    )
                )
            # if is_super_user:
            #     CustomUser.objects.create_superuser(**cur_user)
            # else:
            #     CustomUser.objects.get_or_create(**cur_user)
            # print(f'Пользователь {username} успешно создан')
        CustomUser.objects.bulk_create(model_users)
        print("Пользователи успешно созданы")

    def __generate_phones(self) -> None:
        def get_phone() -> str:
            first = str(random.randint(100, 999))
            second = str(random.randint(1, 888)).zfill(3)
            last = (str(random.randint(1, 9998)).zfill(4))
            template: List[str] = [
                '1111', '2222',
                '3333', '4444',
                '5555', '6666',
                '7777', '8888'
            ]
            while last in template:
                last = (str(random.randint(1, 9998)).zfill(4))
            return '+7{}{}{}'.format(first, second, last)

        user_number: int = CustomUser.objects.count()
        all_users: Tuple[CustomUser] = tuple(CustomUser.objects.all())
        all_models: List[Phone] = []

        _: int
        for _ in range(user_number):
            phone_number: str = get_phone()
            owner: CustomUser = random.choice(all_users)
            all_models.append(
                Phone(
                    phone=phone_number,
                    owner=owner
                )
            )
        Phone.objects.bulk_create(all_models)

    def __generate_friends(self) -> None:
        total_users: int = CustomUser.objects.count()
        all_users_id: Sequence[int] = CustomUser.objects.all().values_list(
            "id",
            flat=True
        )

        friends_model: List[Friends] = []

        i: int
        for i in range(total_users):
            to_user_limit: int = random.randint(2, 10)
            friends: List[int] = all_users_id.exclude(
                id=all_users_id[i]
            )[:to_user_limit]

            k: int
            for k in range(to_user_limit):
                friends_model.append(
                    Friends(
                        from_user_id=all_users_id[i],
                        to_user_id=friends[k],
                        is_blocked=False
                    )
                )
        Friends.objects.bulk_create(friends_model)

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
