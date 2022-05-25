from typing import Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest

from auths.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)
from auths.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # noqa
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        ('Information', {
            'fields': (
                'email',
                'password',
                'username',
                'slug',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_superuser',
                'is_staff',
                'is_active',
            )
        }),
    )
    # NOTE: Used to define the fields that
    #       will be displayed on the create-user page
    #
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'username',
                'slug',
                'birthday',
                'password1',
                'password2',
                'is_active',
            ),
        }),
    )
    search_fields = (
        'email',
        'slug',
    )
    readonly_fields = (
        'datetime_deleted',
        'datetime_created',
        'datetime_updated',
        'is_superuser',
        'is_staff',
        'is_active',
    )
    list_display = (
        'email',
        'password',
        'username',
        'is_staff',
        'slug',
        'is_active',
        'datetime_deleted',
        'datetime_created',
        'datetime_updated',
    )
    list_filter = (
        'email',
        'is_superuser',
        'is_staff',
        'is_active',
    )
    ordering = (
        'email',
    )
    # fields = (
    #     ('id', 'slug'),
    #     'username', 'email',
    #     'password', 'last_login',
    #     'is_superuser',
    #     'datetime_deleted',
    #     'datetime_created',
    #     'datetime_updated',
    # )
    prepopulated_fields = {
        "slug": ("username",),
    }

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[CustomUser] = None
    ) -> tuple:  # noqa
        if not obj:
            return self.readonly_fields

        return self.readonly_fields + (
            'email',
        )
