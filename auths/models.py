from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from abstracts.models import AbstractDateTime


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
        verbose_name='Почта/Логин',
        unique=True
    )
    is_active = models.BooleanField(
        'Активность',
        default=True
    )
    is_staff = models.BooleanField('Статус менеджера', default=False)
    friends = models.ManyToManyField(
        'self',
        blank=True,
        null=True
    )
    blocked_users = models.ManyToManyField(
        "self",
        blank=True,
        null=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:  # noqa
        ordering = (
            'date_joined',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
