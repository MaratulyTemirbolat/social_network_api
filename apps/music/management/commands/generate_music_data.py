from io import TextIOWrapper
import json
from datetime import datetime
from typing import (
    Optional,
    Tuple,
    Any,
    Dict,
    List,
)
from random import (
    choices,
    randint,
)
from names import (
    get_first_name,
    get_last_name
)

from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.utils.text import slugify

from music.models import (
    Playlist,
    Performer,
)
from auths.models import CustomUser


class Command(BaseCommand):
    """Custom command for filling up database.

    Generate Test data only for database.
    For each App you create another own Command
    """

    help = 'Custom command for filling up database.'

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:  # noqa
        super().__init__(args, kwargs)

    def __generate_playlists(
        self,
        playlist_data: Dict[str, List[Dict[str, Any]]]
    ) -> None:
        """Generate of playlist data."""

        def add_listeners(
            listeners: List[CustomUser],
            playlist: Playlist
        ) -> None:
            item: CustomUser
            for item in listeners:
                playlist.listeners.add(item)

        def get_random_listeners(
            existed_users: QuerySet
        ) -> List[CustomUser]:
            k: int = randint(
                0,
                existed_users.count()
            )
            random_listeners: List[CustomUser] = choices(
                existed_users,
                k=k
            )
            return random_listeners

        existed_users: QuerySet = CustomUser.objects.get_not_deleted()

        _: str
        value: List[Dict[str, Any]]
        data: Dict[str, Any]
        for _, value in playlist_data.items():
            for data in value:
                name: str = data.get("text", None)
                if name:
                    random_listeners: List[CustomUser] = get_random_listeners(
                        existed_users=existed_users
                    )

                    new_playlist: Playlist
                    created: bool
                    new_playlist, created = Playlist.objects.get_or_create(
                        name=name,
                    )
                    if created:
                        add_listeners(random_listeners, new_playlist)
        print("Все Плэйлисты успешно созданы!")

    def __generate_performers(
        self,
        performers_data: Dict[str, List[Dict[str, Any]]]
    ) -> None:
        _: str
        value: List[Dict[str, Any]]
        for _, value in performers_data.items():
            item: Dict[str, Any]
            for item in value:
                username: str = item.get("text", None)
                if username:
                    slug: str = slugify(username)
                    name: str = get_first_name()
                    surname: str = get_last_name()
                    if not Performer.objects.filter(slug=slug).exists():
                        Performer.objects.create(
                            username=username,
                            slug=slug,
                            name=name,
                            surname=surname
                        )
        print("Все Исполнители успешно созданы")

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        # Автоматически вызывается, когда вызывается generate_data файл
        """Handle data filling."""
        start: datetime = datetime.now()

        # Получаем время в начале срабатывания кода, чтобы высчитать разницу
        file_path_a: str = '/home/temirbolat/Desktop/files/ITStep/'
        file_path_b: str = 'Django/Diploma/social_network/social_'
        file_path_c: str = 'network_api/apps/music/management/commands/'
        performers_file: str = 'performers.json'
        playlists_file: str = 'playlists.json'
        try:
            data_file_performers: TextIOWrapper = open(
                file_path_a + file_path_b + file_path_c + performers_file
            )
            data_file_playlists: TextIOWrapper = open(
                file_path_a + file_path_b + file_path_c + playlists_file
            )
            data_performers: Dict[str, List[str]] = json.load(
                data_file_performers
            )
            data_playlists: Dict[str, List[str]] = json.load(
                data_file_playlists
            )

            self.__generate_playlists(data_playlists)
            self.__generate_performers(data_performers)
        except Exception as e:
            print("Ошибка при открытии файла")
            print(e)
        finally:
            data_file_performers.close()
            data_file_playlists.close()
            # Выдаем время генерации данных
            print(
                'Генерация данных составила: {} секунд'.format(
                    (datetime.now()-start).total_seconds()
                )
            )
