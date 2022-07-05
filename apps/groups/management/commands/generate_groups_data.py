import random
from datetime import (
    datetime,
)
from typing import (
    List,
    Sequence,
    Tuple,
    Any,
    Dict,
)

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from auths.models import (
    CustomUser,
)
from groups.models import (
    Group,
    GroupAdministration,
    Role,
)


class Command(BaseCommand):
    """Custom command for filling up database.

    Generate Test data only for database.
    For each App you create another own Command
    """

    help = 'Custom command for filling up database.'

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:  # noqa
        super().__init__(args, kwargs)

    def __generate_groups(self, required_number: int = 0) -> None:  # noqa
        def get_group_name(index: int):
            return f"Group {index}"

        def get_group_slug(index: int):
            return slugify(f"Group {index}")

        all_users_id: Sequence[int] = CustomUser.objects.\
            filter(datetime_deleted__isnull=True).values_list(
                "id",
                flat=True
            )

        user_number: int = all_users_id.count()
        groups_model: List[Group] = []

        i: int
        for i in range(required_number):
            name: str = get_group_name(i)
            slug: str = get_group_slug(i)
            # random_start: int = random.randint(0, user_number)
            # random_end: int = random.randint(random_start, user_number)
            # followers: List = all_users_id[random_start:random_end]
            cur_group: Group = Group(
                id=i+1,
                name=name,
                slug=slug
            )
            # for k in followers:
            #     cur_group.followers.append(k)
            groups_model.append(
                cur_group
            )

        Group.objects.bulk_create(groups_model)
        print("Все группы успешно созданы")

    def __generate_group_administrations(
        self,
        required_number: int = 0
    ) -> None:  # noqa
        all_groups_id: Sequence[int] = Group.objects.\
            get_not_deleted().values_list(
                "id",
                flat=True
            )
        all_users_id: Sequence[int] = CustomUser.objects.\
            filter(datetime_deleted__isnull=True).values_list(
                "id",
                flat=True
            )
        all_roles_id: Sequence[int] = Role.objects.\
            get_not_deleted().values_list(
                "id",
                flat=True
            )

        groups_number: int = all_groups_id.count()
        users_number: int = all_users_id.count()
        roles_number: int = all_roles_id.count()

        ZERO_VALUE = 0

        _: int
        for _ in range(required_number):

            ran_group_index: int = random.randint(
                ZERO_VALUE,
                groups_number - 1
            )
            ran_user_index: int = random.randint(
                ZERO_VALUE,
                users_number - 1
            )
            ran_role_index: int = random.randint(
                ZERO_VALUE,
                roles_number - 1
            )

            GroupAdministration.objects.get_or_create(
                group_id=all_groups_id[ran_group_index],
                user_id=all_users_id[ran_user_index],
                role_id=all_roles_id[ran_role_index]
            )

        print("Вся Администрация групп успешно создана")

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        # Автоматически вызывается, когда вызывается generate_data файл
        """Handle data filling."""
        GROUPS_NUMBER = 50
        GROUPS_ADMINISTRATION_NUMBER = 150

        # Получаем время в начале срабатывания кода, чтобы высчитать разницу
        start: datetime = datetime.now()

        # self.__generate_groups(GROUPS_NUMBER)
        # self.__generate_group_administrations(GROUPS_ADMINISTRATION_NUMBER)

        # Выдаем время генерации данных
        print(
            'Генерация данных составила: {} секунд'.format(
                (datetime.now()-start).total_seconds()
            )
        )
