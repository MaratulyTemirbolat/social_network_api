from io import TextIOWrapper
import json
from datetime import datetime
from typing import (
    Tuple,
    Any,
    Dict,
    List,
)

from django.core.management.base import BaseCommand

from locations.models import (
    Country,
    City
)


class Command(BaseCommand):
    """Custom command for filling up database.
    Generate Test data only for database.
    For each App you create another own Command.
    """

    help = 'Custom command for filling up database.'

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:  # noqa
        super().__init__(args, kwargs)

    def __generate_countries_cities_messages(
        self,
        json_data: Dict[str, List[str]]
    ) -> None:
        """Generate countries and cities."""
        ZERO_NUMBER = 0
        existed_countries: int = Country.objects.count()

        if existed_countries == ZERO_NUMBER:
            resulted_cities: List[City] = []
            country_name: str
            cities: List[str]
            cur_city_name: int
            for country_name, cities in json_data.items():
                new_country: Country
                is_created: bool
                new_country, is_created = Country.objects.get_or_create(
                    name=country_name
                )
                is_capital: bool = True
                for cur_city_name in cities:
                    resulted_cities.append(
                        City(
                            name=cur_city_name,
                            country_id=new_country.id,
                            is_capital=is_capital
                        )
                    )
                    if is_capital:
                        is_capital = False
            City.objects.bulk_create(resulted_cities)
            print("Все страны и города были созданы!")

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        # Автоматически вызывается, когда вызывается generate_data файл
        """Handle data filling."""
        start: datetime = datetime.now()
        # Получаем время в начале срабатывания кода, чтобы высчитать разницу
        file_path_part_a: str = '/home/temirbolat/Desktop/files/ITStep/Django'
        file_path_part_b: str = '/Diploma/social_network/social_network_api'
        file_path_part_c: str = '/apps/locations/management/commands/data.json'
        data_file: TextIOWrapper = open(
            file_path_part_a + file_path_part_b + file_path_part_c
        )
        data: Dict[str, List[str]] = json.load(data_file)

        self.__generate_countries_cities_messages(data)

        # Выдаем время генерации данных
        print(
            'Генерация данных составила: {} секунд'.format(
                (datetime.now()-start).total_seconds()
            )
        )
