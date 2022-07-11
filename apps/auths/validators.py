from datetime import date

from django.core.exceptions import ValidationError


def the_same_users_validator(
    user_a,
    user_b
) -> None:  # noqa
    if not user_a or not user_b:
        raise ValidationError("Нужно обеспечить двух разных пользователей")
    if user_a.id == user_b.id:
        raise ValidationError("Вы не можете добавить самого себя в друзья")


def adult_validation(age: date) -> None:
    """Validate the age to be more than 18."""
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


def email_lower_case_validation(email: str) -> None:
    """Validate upper case of the email."""
    if(any(letter.isupper() for letter in email)):
        raise ValidationError(
            "Почта не может иметь ни один символ в верхнем регистре",
            code='lower_case_email_error'
        )


def username_space_validation(username: str) -> None:
    """Validate username for whitespaces."""
    if username.count(" ") > 0:
        raise ValidationError(
            message="Никнейм не должен иметь никаких пробелов",
            code="username_whitespace_error"
        )
