from typing import (
    Sequence,
    Tuple,
    Any,
    Optional,
)

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from groups.models import (
    Group,
    Privilege,
    Role,
    GroupAdministration,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(Group)
class GroupModel(admin.ModelAdmin):  # noqa
    readonly_fields: Sequence[str] = (
        "datetime_deleted",
        "datetime_updated",
        "datetime_created",
    )
    fieldsets: Tuple = (
        ('Информация о группе', {
            'fields': (
                'name',
                'slug',
            )
        }),
        ('Подписчики', {
            'fields': (
                'followers',
            )
        }),
        ('История группы', {
            'fields': (
                'datetime_deleted',
                'datetime_created',
                'datetime_updated',
            )
        })
    )
    filter_horizontal: Sequence[str] = (
        'followers',
    )
    list_display: Tuple[str] = (
        "id",
        'name',
        'slug',
        "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    ordering: Optional[Sequence[str]] = (
        '-datetime_updated',
    )
    save_on_top: bool = True
    search_fields: Tuple[str] = (
        "name", "slug",
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Group] = None
    ) -> Sequence[str]:  # noqa
        if obj:
            return self.readonly_fields + ("followers",)
        return self.readonly_fields

    def get_is_deleted(self, obj: Optional[Group]=None) -> str:  # noqa
        if obj.datetime_deleted:
            return "Группа удалена"
        return "Группа не удалена"
    get_is_deleted.short_description = "Существование группы"
    get_is_deleted.empty_value_display = "Группа не удалена"


@admin.register(Privilege)
class PrivilegeModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_updated",
        "datetime_created",
        "slug",
    )
    list_display: Tuple[str] = (
        "name_en", "name_ru",
        "slug", "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    list_display_links: Tuple[str] = (
        "name_en", "name_ru", "slug",
    )
    save_as_continue: bool = True

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Privilege] = None
    ) -> Tuple[str]:  # noqa
        if obj:
            return self.readonly_fields + ("name_en", "slug",)
        return self.readonly_fields

    def get_is_deleted(self, obj: Optional[Privilege]=None) -> str:  # noqa
        if obj.datetime_deleted:
            return "Привилегия удалена"
        return "Привилегия не удалена"
    get_is_deleted.short_description = "Существование привилегии"
    get_is_deleted.empty_value_display = "Привилегия не удалена"


@admin.register(Role)
class RoleModel(admin.ModelAdmin):  # noqa
    readonly_fields: Sequence[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "name", "slug",
        "get_is_deleted",
    )
    filter_horizontal: Tuple[str] = (
        "privileges",
    )
    list_filter: Tuple[str, Any] = (
        CommonStateFilter,
        "privileges",
    )
    search_fields: Tuple[str] = (
        "name", "slug",
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Role] = None
    ) -> Tuple[str]:  # noqa
        if obj:
            return self.readonly_fields + ("name", "slug",)
        return self.readonly_fields

    def get_is_deleted(self, obj: Optional[Role] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return "Роль удалена"
        return "Роль не удалена"
    get_is_deleted.short_description = "Существование роли"
    get_is_deleted.empty_value_display = "Роль не удалена"


@admin.register(GroupAdministration)
class GroupAdministrationModel(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "id", "group",
        "user", "role",
    )
    list_filter: Tuple[str] = (
        "role",
    )
    list_display_links: Tuple[str] = (
        "id", "group",
    )
    fieldsets: Tuple = (
        ('Информация о группе', {
            'fields': (
                'group',
            )
        }),
        ('Информация о пользователе', {
            'fields': (
                'user',
            )
        }),
        ('Роль в группе', {
            'fields': (
                'role',
            )
        }),
        ('История', {
            'fields': (
                'datetime_deleted',
                'datetime_created',
                'datetime_updated',
            )
        })
    )
