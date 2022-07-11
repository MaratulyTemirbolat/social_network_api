from datetime import date
from typing import (
    Any,
    Optional,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.text import slugify
from django.db import models
from django.db.models import Q
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.core.validators import (
    RegexValidator,
)

from abstracts.models import (
    AbstractDateTime,
    AbstractDateTimeQuerySet,
)
from auths.validators import (
    the_same_users_validator,
    adult_validation,
    email_lower_case_validation,
    username_space_validation,
)


def validate_slug_field(slug: str):
    """Validate slug unique field."""
    if CustomUser.objects.filter(slug=slug).exists():
        raise ValidationError(
            message="Поле slug должно быть уникальным.\
Возможно оно зависит от уникальности другого поля.",
            code="slug_unique_error"
        )


class CustomUserManager(BaseUserManager):
    """CustmoUserManager."""

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        username: str,
        birthday: date,
        **kwargs: dict
    ) -> 'CustomUser':  # noqa

        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            username=username,
            birthday=birthday,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        username: str,
        birthday: date,
        **kwargs: dict
    ) -> 'CustomUser':  # noqa

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            username=username,
            birthday=birthday,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_not_deleted(self) -> QuerySet:
        """Get NON-deleted users."""
        return self.filter(datetime_deleted__isnull=True)

    def get_deleted(self) -> QuerySet:
        """Get deleted users."""
        return self.filter(datetime_deleted__isnull=False)

    def get_active_users(self) -> QuerySet:
        """Get active users."""
        return self.get_not_deleted().filter(is_active=True)

    def get_active_administrators(self) -> QuerySet:
        """Get active administrators."""
        return self.get_not_deleted().filter(
            is_active=True,
            is_superuser=True
        )


YOU_BLOCKED_STATE = 1
YOU_ARE_BLOCKED_STATE = 2
ALREADY_FRIENDS_STATE = 3
ALREADY_REQUEST_SENT_STATE = 4


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractDateTime
):
    """CustomUser model."""

    PERSONAL_DATA_MAX_LEN = 150

    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[email_lower_case_validation],
        verbose_name='Почта/Логин'
    )
    first_name = models.CharField(
        max_length=PERSONAL_DATA_MAX_LEN,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=PERSONAL_DATA_MAX_LEN,
        verbose_name="Фамилия"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активность',
        help_text="True - ваш аккаунт активный, False - удален"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус менеджера'
    )
    friendss = models.ManyToManyField(
        to='self',
        blank=True,
        through="Friends",
        symmetrical=False,
        verbose_name="Друзья",
        related_name="following"
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name="Последний вход"
    )
    is_online = models.BooleanField(
        default=False,
        verbose_name="Онлайн"
    )
    username = models.CharField(
        max_length=PERSONAL_DATA_MAX_LEN,
        unique=True,
        validators=[username_space_validation],
        verbose_name="Никнейм"
    )
    slug = models.SlugField(
        max_length=PERSONAL_DATA_MAX_LEN,
        unique=True,
        verbose_name="Url (by username)",
        db_index=True,
        validators=[validate_slug_field],
        help_text="URL по юзернейму которого происходит поиск"
    )
    birthday = models.DateField(
        validators=[adult_validation],
        verbose_name="Дата рождения"
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        "username", "first_name",
        "last_name", "birthday"
    ]

    objects = CustomUserManager()

    class Meta:
        """Customization of the Model."""

        ordering = (
            '-datetime_updated',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # noqa
        return f'ID:{self.id} Пользователь: {self.username}'


class FriendsQuerySet(QuerySet):
    """FriendsQuerySet."""

    def get_friends(
        self,
        from_user: CustomUser,
        to_user: CustomUser
    ) -> Optional[Any]:
        """Get friends model instance if it is existed."""
        try:
            friends_pair: 'Friends' = self.get(
                from_user=from_user,
                to_user=to_user
            )
            return friends_pair
        except Exception:
            return None

    def __handle_friends_state(
        self,
        from_user: CustomUser,
        pair: 'Friends'
    ) -> Optional[int]:
        """Get state of the friends."""
        if pair.is_blocked:
            if pair.from_user == from_user:
                return YOU_BLOCKED_STATE
            return YOU_ARE_BLOCKED_STATE
        else:
            if pair.from_user == from_user:
                return ALREADY_REQUEST_SENT_STATE
        return None

    def get_friends_state(
        self,
        from_user: CustomUser,
        to_user: CustomUser
    ) -> Optional[int]:
        """Handle friends state."""
        friends_pair: QuerySet = self.filter(
            Q(from_user=from_user, to_user=to_user) |
            Q(from_user=to_user, to_user=from_user)
        )
        friends_number: int = friends_pair.count()
        if friends_number == 0:
            return None
        elif friends_number == 1:
            pair_first: 'Friends' = friends_pair.first()
            return self.__handle_friends_state(
                from_user=from_user,
                pair=pair_first
            )
        else:
            pair_first: 'Friends' = friends_pair.first()
            pair_last: 'Friends' = friends_pair.last()
            first_pair_state: Optional[int] = self.__handle_friends_state(
                from_user=from_user,
                pair=pair_first
            )
            last_pair_state: Optional[int] = self.__handle_friends_state(
                from_user=from_user,
                pair=pair_last
            )

            if (first_pair_state == ALREADY_REQUEST_SENT_STATE and
                not last_pair_state) or \
                    (not first_pair_state and
                        last_pair_state == ALREADY_REQUEST_SENT_STATE):
                return ALREADY_FRIENDS_STATE
            if first_pair_state:
                return first_pair_state
            if last_pair_state:
                return last_pair_state
        return ALREADY_FRIENDS_STATE


class Friends(models.Model):
    """Friends Model."""

    from_user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Текущий пользователь",
    )
    to_user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Кого добавляет"
    )
    is_blocked = models.BooleanField(
        default=False,
        verbose_name="Заблокирован"
    )
    objects = FriendsQuerySet.as_manager()

    class Meta:
        """Customization of the Model."""

        verbose_name_plural = "Друзья"
        verbose_name = "Друг"
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["from_user", "to_user"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        ]

    def __str__(self) -> str:  # noqa
        return f'Пользователь {self.from_user} подписался на {self.to_user}'

    def clean(self) -> None:  # noqa
        the_same_users_validator(self.from_user, self.to_user)
        return super().clean()

    def save(self, *args: tuple, **kwargs: dict) -> None:  # noqa
        self.full_clean()
        super().save(*args, **kwargs)


class PhoneQuerySet(AbstractDateTimeQuerySet):
    """PhoneQuerySet."""

    pass


class Phone(AbstractDateTime):
    """Phone Model."""

    phone = models.CharField(
        max_length=12,
        verbose_name="Номер телефона",
        validators=[
            RegexValidator(
                regex="^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7}$",  # noqa
                message="Формат вашего телефона не совпадает",
                code="phone_format"
            )
        ],
        unique=True,
        db_index=True,
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="phones",
        verbose_name="Владелец"
    )
    objects = PhoneQuerySet.as_manager()

    class Meta:
        """Customization of the Model."""

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
