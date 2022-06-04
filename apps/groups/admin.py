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
