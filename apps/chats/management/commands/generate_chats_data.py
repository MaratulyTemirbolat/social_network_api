from random import (
    randint,
    choice,
    choices,
    sample,
)
from datetime import datetime
from typing import (
    Tuple,
    Any,
    Dict,
    List,
    Optional,
)

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db.models import QuerySet

from auths.models import CustomUser
from chats.models import (
    Chat,
    ChatMember,
    Message,
)
from abstracts.models import AbstractDateTimeQuerySet


class Command(BaseCommand):
    """Custom command for filling up database.

    Generate Test data only for database.
    For each App you create another own Command
    """

    help = 'Custom command for filling up database.'

    __chats_templates: Tuple[str] = (
        "FIT", "BS", "ISE", "MCM",
        "Anime", "Films", "Sky fi",
        "No name", "Group", "Calculus",
        "Hentai", "Books", "Role play",
    )
    __is_group_list: Tuple[bool] = (
        True, False,
    )
    __message_template_parts: Tuple[str] = (
        "hello", "world", "animal", "person",
        "good", "thank you", "nice", "show", "say",
        "anime", "Turkey", "Canada", "Kazakhstan", "dear",
        "bird", "dog", "cat", "queen", "buy", "sir", "apple",
        "pear", "zebra", "man", "girl", "boy", "Russia",
        "Paris", "United Kingdom", "boyfriend", "girlfriend",
        "Kaneki", "John", "Temirbolat", "Mike", "Marat", "Rem",
        "Ram", "laptop", "computer", "mouse", "lorem impsum",
        "Almaty", "Moscow", "Astana", "Karaganda", "NU", "KBTU",
        "or", "and", "as well as", "along with", "while", "including",
    )

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:  # noqa
        super().__init__(args, kwargs)

    def __generate_chats(self, chats_number: int = 0) -> None:
        """Chats generation with required quantity."""
        chats_templates_len: int = len(self.__chats_templates)

        def generate_name(index: int) -> str:
            """Get new name of group with index."""
            ran_index: int = randint(0, chats_templates_len - 1)
            ran_group_tem: str = self.__chats_templates[ran_index]
            return f"{ran_group_tem} {index}"

        def get_is_group() -> bool:
            return choice(self.__is_group_list)

        existed_chats: int = Chat.objects.count()

        groups: List[Chat] = []

        _: int
        for _ in range(chats_number):
            existed_chats += 1
            name: str = generate_name(existed_chats)
            slug: str = slugify(name)
            is_group: bool = get_is_group()
            groups.append(
                Chat(
                    name=name,
                    slug=slug,
                    is_group=is_group
                )
            )
        Chat.objects.bulk_create(groups)
        print(f"{chats_number} чат(-а, -ов) успешно созданы")

    def __generate_chat_members(self) -> None:
        all_chats_data: AbstractDateTimeQuerySet[Tuple[int, bool]] = Chat.\
            objects.get_not_deleted().values_list(
                "id",
                "is_group"
        )
        all_chats_number: int = all_chats_data.count()
        all_users: QuerySet = CustomUser.objects.\
            get_not_deleted().values_list(
                "id", flat=True
            )

        GROUP_CHAT_MAX_PEOPLE = 10
        GROUP_CHAT_MIN_PEOPLE = 3
        NON_GROUP_CHAT_MAX_PEOPLE = 2

        def generate_group_members(chat_id: int) -> None:
            ran_people_number: int = randint(
                GROUP_CHAT_MIN_PEOPLE,
                GROUP_CHAT_MAX_PEOPLE
            )
            ran_member_list: List[Tuple[int, bool]] = choices(
                all_users,
                k=ran_people_number
            )

            k: int
            for k in range(ran_people_number):
                ChatMember.objects.get_or_create(
                   chat_id=chat_id,
                   user_id=ran_member_list[k]
                )

        def generate_non_group_members(chat_id: int) -> None:
            ran_members_list: List[Tuple[int, bool]] = choices(
                all_users,
                k=NON_GROUP_CHAT_MAX_PEOPLE
            )

            ran_members_list = [
                ChatMember(
                    chat_id=chat_id,
                    user_id=ran_members_list[0]
                ),
                ChatMember(
                    chat_id=chat_id,
                    user_id=ran_members_list[1]
                )
            ]

            ChatMember.objects.bulk_create(ran_members_list)

        i: int
        for i in range(all_chats_number):
            chat_id: int = all_chats_data[i][0]
            is_group: bool = all_chats_data[i][1]
            if is_group:
                generate_group_members(chat_id=chat_id)
            else:
                generate_non_group_members(chat_id=chat_id)

        print(f"Все Члены {all_chats_number} чат(-ов, а) успешно созданы")

    def __generate_chat_messages(self) -> None:
        MIN_CONTENT_WORDS_NUM = 5
        MAX_CONTENT_WORDS_NUM = 30

        chat_list_id: AbstractDateTimeQuerySet = Chat.objects.\
            get_not_deleted().values_list(
                "id",
                flat=True
            )
        chats_number: int = chat_list_id.count()
        chat_members: Optional[QuerySet] = None

        messages_list: List[Message] = []

        def get_random_content() -> str:
            ran_words_number: int = randint(
                MIN_CONTENT_WORDS_NUM,
                MAX_CONTENT_WORDS_NUM
            )
            return ' '.join(
                sample(
                    population=self.__message_template_parts,
                    k=ran_words_number
                )
            ).capitalize()

        i: int
        k: int
        for i in range(chats_number):
            message_number: int = randint(1, 8)
            chat_id: int = chat_list_id[i]
            chat_members = ChatMember.objects.filter(
                chat_id=chat_id
            ).values_list("user_id", flat=True)

            for k in range(message_number):
                content: str = get_random_content().replace(
                    ' ',
                    ', ',
                    4
                )
                owner_id: int = choice(chat_members)
                messages_list.append(
                    Message(
                        content=content,
                        chat_id=chat_id,
                        owner_id=owner_id
                    )
                )
        Message.objects.bulk_create(messages_list)
        print(
            f"Все сообщения для {chats_number} чат(-ов, -а) успешно созданы"
        )

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        # Автоматически вызывается, когда вызывается generate_data файл
        """Handle data filling."""
        CHATS_NUMBER = 25

        start: datetime = datetime.now()
        # Получаем время в начале срабатывания кода, чтобы высчитать разницу

        self.__generate_chats(CHATS_NUMBER)
        self.__generate_chat_members()
        self.__generate_chat_messages()

        # Выдаем время генерации данных
        print(
            'Генерация данных составила: {} секунд'.format(
                (datetime.now()-start).total_seconds()
            )
        )
