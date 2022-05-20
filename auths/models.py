from datetime import date

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from abstracts.models import AbstractDateTime


def adult_validation(age: date) -> None:  # noqa
    ADULT_AGE = 18
    today: date = date.today()
    cur_age: int = today.year - age.year - (
        (today.month, today.day) < (age.month, age.day)
    )
    if cur_age < ADULT_AGE:
        raise ValidationError(
            "Ваш возраст не может быть меньше 18 лет (функция валидатор)",
            code='adult_age_error'
        )


def email_lower_case_validation(email: str) -> None:  # noqa
    if(any(letter.isupper() for letter in email)):
        raise ValidationError(
            "Почта не может иметь ни один символ в верхнем регистре",
            code='lower_case_email_error'
        )


class CustomUserManager(BaseUserManager):  # noqa

    def create_user(
        self,
        email: str,
        password: str
    ) -> 'CustomUser':  # noqa

        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'CustomUser':  # noqa

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_non_deleted(self) -> QuerySet:  # noqa
        return self.filter(datetime_deleted__isnull=True)


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractDateTime
):  # noqa
    email = models.EmailField(
        unique=True,
        validators=[email_lower_case_validation],
        verbose_name='Почта/Логин'
    )
    is_active = models.BooleanField(
        'Активность',
        default=True
    )
    is_staff = models.BooleanField('Статус менеджера', default=False)
    friends = models.ManyToManyField(
        to='self',
        blank=True,
        null=True
    )
    blocked_users = models.ManyToManyField(
        to="self",
        blank=True,
        null=True
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name="Последний вход"
    )
    is_online = models.BooleanField(
        default=True,
        verbose_name="Онлайн"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Никнейм"
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        verbose_name="Url"
    )
    birthday = models.DateField(
        validators=[adult_validation],
        verbose_name="Дата рождения"
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "birthday"]

    objects = CustomUserManager()

    class Meta:  # noqa
        ordering = (
            'date_joined',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
