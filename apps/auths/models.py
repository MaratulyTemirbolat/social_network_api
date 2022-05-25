from datetime import date
# from autoslug import AutoSlugField

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.text import slugify
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
        password: str,
        username: str,
        birthday: date
    ) -> 'CustomUser':  # noqa

        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
            birthday=birthday
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        username: str,
        birthday: date
    ) -> 'CustomUser':  # noqa

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
            birthday=birthday
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
        default=True,
        verbose_name='Активность'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус менеджера'
    )
    friends = models.ManyToManyField(
        to='self',
        blank=True,
        verbose_name="Друзья"
    )
    blocked_users = models.ManyToManyField(
        to='self',
        blank=True,
        verbose_name="Заблокированные пользователи"
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
        max_length=255,
        unique=True,
        verbose_name="Url (by username)"
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
            'datetime_created',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f'Пользователь: {self.username}; Email: {self.email}'


class Phone(AbstractDateTime):  # noqa
    phone = models.CharField(
        max_length=12,
        verbose_name="Номер телефона"
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.RESTRICT,
        related_name="phones",
        verbose_name="Владелец"
    )

    class Meta:  # noqa
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        ordering = (
            'datetime_created',
        )
        constraints = [
            models.UniqueConstraint(
                fields=['phone', 'owner'],
                name="unique_phone_owner"
            ),
        ]

    def __str__(self) -> str:  # noqa
        return f'Телефон {self.phone} принадлежит {self.owner}'
