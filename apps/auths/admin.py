from typing import (
    Optional,
    Tuple,
    Dict,
    Sequence,
    Any,
)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest

# from auths.forms import (
#     CustomUserCreationForm,
#     CustomUserChangeForm,
# )
from auths.models import (
    CustomUser,
    Friends,
)
from auths.filters import CommonStateFilter


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # noqa
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = CustomUser

    fieldsets: Tuple = (
        ('Личная инормация', {
            'fields': (
                'email',
                ('username', 'slug'),
                ('first_name', 'last_name'),
                'birthday',
                'password',
            )
        }),
        ('Разрешения (Доступы)', {
            'fields': (
                'is_superuser',
                'is_staff',
                'is_active',
                'is_online',
                'user_permissions',
            )
        }),
        # ('Взаимодействие с пользователями', {
        #     'fields': (
        #         'friendss',
        #     )
        # }),
        ('Данные времени', {
            'fields': (
                'last_login',
                'last_seen',
                'datetime_deleted',
                'datetime_created',
                'datetime_updated',
            )
        })
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
    search_fields: Tuple[str] = (
        'email',
        'slug',
        'username',
    )
    readonly_fields: Tuple[str] = (
        'is_superuser',
        'is_staff',
        'is_active',
        'last_seen',
        'is_online',
        'last_login',
        'datetime_deleted',
        'datetime_created',
        'datetime_updated',
    )
    list_display: Tuple[str] = (
        'email',
        'username',
        'slug',
        'is_staff',
        'is_active',
        'last_login',
    )
    list_filter: Tuple[str, Any] = (
        'is_superuser',
        'is_staff',
        'is_active',
        CommonStateFilter,
    )
    ordering: Tuple[str] = (
        'email',
    )
    save_on_top: bool = True
    prepopulated_fields: Dict[str, Sequence[str]] = {
        "slug": ("username",),
    }
    filter_horizontal: Sequence[str] = (
        "user_permissions",
    )

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


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):  # noqa
    pass
