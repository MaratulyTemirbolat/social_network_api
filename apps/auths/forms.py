from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from auths.models import CustomUser


class CustomUserCreationForm(UserCreationForm):  # noqa

    class Meta:  # noqa
        model = CustomUser
        fields = (
            'email',
        )


class CustomUserChangeForm(UserChangeForm):  # noqa

    class Meta:  # noqa
        model = CustomUser
        fields = (
            'email',
        )


class CustomUserForm(forms.ModelForm):  # noqa
    email = forms.EmailField(
        label='Почта'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль'
    )

    class Meta:  # noqa
        model = CustomUser
        fields = (
            'email',
            'password',
        )
