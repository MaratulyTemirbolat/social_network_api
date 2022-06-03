import random
import names
from datetime import datetime
from typing import (
    Tuple,
    Any,
    Dict,
)

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    User,
)

from my_new_app.models import (
    Group,
    Account,
    Student,
    Professor,
    StudentQuerySet,
)


class Command(BaseCommand):
    """Custom command for filling up database.

    Generate Test data only for database. 
    For each App you create another own Command
    """
    help = 'Custom command for filling up database.'

    _email_patterns: tuple = (
        'gmail.com', 'outlook.com', 'yahoo.com',
        'inbox.ru', 'inbox.ua', 'inbox.kz',
        'yandex.ru', 'yandex.ua', 'yandex.kz',
        'mail.ru', 'mail.ua', 'mail.kz',
    )
    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:  # noqa
        super().__init__(args, kwargs)

    def __generate_name(self,
                        name: str,
                        inc: int) -> str:
        return f'{name} {inc}'

    def _generate_users(self, user_number: int,
                        initial_time: datetime) -> None:
        """Generate user objects"""

        REQUIRED_SUPERUSER_QUANTITY = 1

        def get_username(first_name: str, last_name: str) -> str:
            username: str = first_name.lower() + '_' + last_name.lower()
            return username

        def get_email(first_name: str, last_name: str) -> str:
            email_identification: str = random.choice(_email_patterns)
            email: str = first_name.lower() + '.' + last_name.lower() + \
                '@' + email_identification
            return email

        def get_password() -> str:
            _passwd_pattern: str = 'abcde12345'
            _passwd_length: int = 8
            _user_password: str = ''.join(
                random.sample(_passwd_pattern, _passwd_length)
                )
            return make_password(_user_password)
        
        def get_user_instance_dict() -> dict:
            first_name: str = names.get_first_name()
            last_name: str = names.get_last_name()
            username: str = get_username(first_name, last_name)
            email: str = get_email(first_name, last_name)
            password: str = get_password()
            
            cur_user: dict = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': password,
                'is_staff': True,
            }

            return cur_user

        super_user_number: int = User.objects.filter(
            is_superuser=True
            ).count()

        if (super_user_number < REQUIRED_SUPERUSER_QUANTITY):
            super_user: dict = get_user_instance_dict()
            while(User.objects.filter(
                username=super_user['username']
            ).exists()):
                super_user = get_user_instance_dict()

            super_user['is_superuser'] = True
            User.objects.create(**super_user)
            user_number -= 1
            print(
                'Generating Data for SuperUser: {} seconds'.format(
                 (datetime.now()-initial_time).total_seconds()
                )
            )

        cur_user: dict = get_user_instance_dict()

        cur_index: int
        for cur_index in range(user_number):
            while(User.objects.filter(
                  username=cur_user['username']
                  ).exists()):
                cur_user = get_user_instance_dict()

            User.objects.create(**cur_user)
            print(
                 'Generating Data for General User: {} seconds'.format(
                  (datetime.now()-initial_time).total_seconds()
                 )
            )

    def _generate_users_accounts_students(self) -> None:
        """Generate user account and student objects"""

        USER_ACCOUNT_STUDENT_NUMBER = 100
        DEFAULT_PASSWORD = '12345'

        def generate_username(increment: int) -> str:
            return f'User {increment}'

        def generate_student_age() -> int:
            random_age: int = random.randint(5, Student.MAX_REGISTER_AGE)
            return random_age

        def get_random_group() -> Group:
            random_group: Group = random.choice(Group.objects.all())
            return random_group

        def get_random_gpa() -> float:
            GPA_MULTIPLIER = 4.0
            HUNDRETH_POSITION = 2
            random_gpa: float = GPA_MULTIPLIER * random.random()
            random_gpa = round(random_gpa, HUNDRETH_POSITION)
            return random_gpa

        increment: int 
        for increment in range(USER_ACCOUNT_STUDENT_NUMBER):
            username: str = generate_username(increment)
            is_staff: bool = True

            created_user: User = User.objects.create(
                username=username,
                is_staff=is_staff,
                password=DEFAULT_PASSWORD
            )

            account_full_name: str = self.__generate_name(username, increment)
            account_description: str = f'{username}\'s description'
            created_account: Account = Account.objects.create(
                user=created_user,
                full_name=account_full_name,
                description=account_description
            )
            student_age: int = generate_student_age()
            student_group: Group = get_random_group()
            student_gpa: float = get_random_gpa()
            Student.objects.create(
                account=created_account,
                age=student_age,
                group=student_group,
                gpa=student_gpa
            )

    def _generate_groups(self) -> None:
        """Generate Group objs."""

        def generate_name(inc: int) -> str:
            return f'Группа {inc}'

        inc: int
        for inc in range(20):
            name: str = generate_name(inc)
            Group.objects.create(
                name=name
            )

    def _generate_professors(self) -> None:
        """Generate Professor objs."""
        PROFESSOR_NUMBER = 10
        MIN_STUDENT_NUMBER = 1
        MAX_STUDENT_NUMBER = 5

        def get_random_subject_topic() -> str:
            all_subjects: tuple = Professor.TOPIC_CHOICES
            random_subject: str = random.choice(all_subjects)[0]
            return random_subject

        inc: int
        for inc in range(PROFESSOR_NUMBER):
            full_name: str = self.__generate_name('Профессор', inc)
            topic: str = get_random_subject_topic()
            created_professor: Professor = Professor.objects.create(
                full_name=full_name,
                topic=topic
            )

            student_number: int = random.randint(
                MIN_STUDENT_NUMBER,
                MAX_STUDENT_NUMBER
                )
            all_students: StudentQuerySet = Student.objects.all()
            unregistered_students: list = random.choices(all_students,
                                                         k=student_number)

            i: int
            for i in range(student_number):
                unregistered_students[i].professor_set.add(
                    created_professor
                    )

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        # Автоматически вызывается, когда вызывается generate_data файл
        """Handles data filling."""

        TOTAL_USER_COUNT = 500
        ZERO_COUNT = 0

        start: datetime = datetime.now()
        # Получаем время в начале срабатывания кода, чтобы высчитать разницу

        current_user_number: int = User.objects.count()
        user_difference: int = TOTAL_USER_COUNT - current_user_number
        if (user_difference > ZERO_COUNT):
            self._generate_users(user_difference, start)
        else:
            print(
                'No need to create Users. Max amount is',
                TOTAL_USER_COUNT
            )

        # self._generate_groups()  # Генерируем данные
        # self._generate_users_accounts_students()
        # self._generate_professors()

        # Выдаем время генерации данных
        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )