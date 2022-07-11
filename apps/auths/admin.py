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
from django.utils.safestring import mark_safe

from auths.models import (
    CustomUser,
    Friends,
    Phone,
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
    add_fieldsets: Tuple = (
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
        'id',
        'email',
        'username',
        'slug',
        'is_staff',
        'is_active',
        'is_superuser',
        'last_login',
        'get_is_deleted',
    )
    list_display_links: Tuple[str] = (
        "id",
        "email",
        "username",
        "slug",
    )
    list_filter: Tuple[str, Any] = (
        'is_superuser',
        'is_staff',
        'is_active',
        CommonStateFilter,
    )
    ordering: Tuple[str] = (
        '-datetime_updated',
    )
    save_on_top: bool = True
    prepopulated_fields: Dict[str, Sequence[str]] = {
        "slug": ("username",),
    }
    filter_horizontal: Sequence[str] = (
        "user_permissions",
    )
    list_per_page: int = 20

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

    def get_is_deleted(self, obj: Optional[CustomUser] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Пользователь удален</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Пользователь не удален</p>'
            )
    get_is_deleted.short_description = "Существование видео"
    get_is_deleted.empty_value_display = "Пользователь не удален"


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):  # noqa
    list_display: Tuple[str] = (
        "id",
        "from_user",
        "to_user",
        "is_blocked",
    )
    list_display_links: Tuple[str] = (
        "id",
        "from_user",
        "to_user",
    )
    list_filter: Tuple[str] = (
        "is_blocked",
    )
    search_fields: Sequence[str] = (
        "from_user__username",
    )


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Sequence[str] = (
        "datetime_deleted",
        "datetime_updated",
        "datetime_created",
    )
    list_display: Tuple[str] = (
        "phone",
        "owner",
    )
    search_fields: Tuple[str] = (
        "phone",
    )
