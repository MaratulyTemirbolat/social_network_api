from django.core.exceptions import ValidationError


def the_same_users_validator(
    user_a,
    user_b
) -> None:  # noqa
    if not user_a or not user_b:
        raise ValidationError("Нужно обеспечить двух разных пользователей")
    if user_a.id == user_b.id:
        raise ValidationError("Вы не можете добавить самого себя в друзья")
