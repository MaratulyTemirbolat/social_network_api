from optparse import Option
from typing import (
    Tuple,
    Any,
    Optional,
    Dict,
)

from django.contrib import admin
from django.utils.safestring import mark_safe

from news.models import (
    Tag,
    Category,
    News,
    Comment,
)
from abstracts.filters import (
    CommonStateFilter,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
        "slug",
    )
    list_display: Tuple[str] = (
        "name", "slug",
        "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    search_fields: Tuple[str] = (
        "name",
        "slug",
    )

    def get_is_deleted(self, obj: Optional[Tag] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Тэг удален</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Тэг не удален</p>'
            )
    get_is_deleted.short_description = "Существование тэга"
    get_is_deleted.empty_value_display = "Тэг не удален"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: Tuple[str] = (
        "slug",
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    list_display: Tuple[str] = (
        "id",
        "title",
        "slug",
        "get_is_deleted",
    )
    search_fields: Tuple[str] = (
        "title",
        "slug",
    )
    list_display_links: Tuple[str] = (
        "title",
        "slug",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )

    def get_is_deleted(self, obj: Optional[Category] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Категория удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Категория не удалена</p>'
            )
    get_is_deleted.short_description = "Существование категории"
    get_is_deleted.empty_value_display = "Категория не удалена"


@admin.register(News)
class NewsModel(admin.ModelAdmin):  # noqa
    fieldsets: Tuple[Tuple[str, Dict[str, Tuple[str]]]] = (
        ('Инормация о новости', {
            'fields': (
                'title',
                'photo',
                'content',
            )
        }),
        ('Категория, тэги, автор, группы', {
            'fields': (
                'group',
                'author',
                'category',
                'tags',
            )
        }),
        ('Лайки пользователей', {
            'fields': (
                'liked_users',
            )
        }),
        ('История новости', {
            'fields': (
                'datetime_created',
                'datetime_deleted',
                'datetime_updated',
            )
        })
    )
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    filter_horizontal: Tuple[str] = (
        "liked_users",
        "tags",
    )
    list_display: Tuple[str] = (
        'id', 'title',
        'get_shorted_content', 'get_photo',
        'get_published_group',
        'get_published_author', 'category',
        'get_is_deleted',
    )
    search_fields: Tuple[str] = (
        'title',
    )
    list_display_links: Tuple[str] = (
        "id", "title",
    )
    list_per_page: int = 20
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    save_on_top: bool = True

    def get_published_author(self, obj:Optional[News] = None) -> str:  # noqa
        if obj.author:
            return f'Опубликовано {obj.author}'
        return 'Не опубликовано пользователем'
    get_published_author.short_description = "Опубликованность пользователем"

    def get_shorted_content(self, obj: Optional[News] = None) -> Optional[str]:  # noqa
        if obj:
            return f'{obj.content[:50]}...'
    get_shorted_content.short_description = "Контент новости"

    def get_published_group(self, obj:Optional[News] = None) -> str:  # noqa
        if obj.group:
            return f'Опубликовано группой {obj.group}'
        return 'Не опубликовано группой'
    get_published_group.short_description = "Опубликованность группой"

    def get_is_deleted(self, obj: Optional[News] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Новость удалена</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Новость не удалена</p>'
            )
    get_is_deleted.short_description = "Существование новости"
    get_is_deleted.empty_value_display = "Новость не удалена"

    def get_photo(self, obj: Optional[News] = None) -> str:  # noqa
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" height="100">')
    get_photo.short_description = "Фотография новости"
    get_photo.empty_value_display = "No photo uploaded"


@admin.register(Comment)
class CommentModel(admin.ModelAdmin):  # noqa
    fieldsets: Tuple[Tuple[str, Dict[str, Tuple[str]]]] = (
        ('Информация о комментарии', {
            'fields': (
                'content',
                'commentator',
                'news',
            ),
        }),
        ('Лайки пользователей на данный комментарий', {
            'fields': (
                'likes',
            ),
        }),
        ('История комментария', {
            'fields': (
                'datetime_created',
                'datetime_deleted',
                'datetime_updated',
            ),
        })
    )
    readonly_fields: Tuple[str] = (
        "datetime_deleted",
        "datetime_updated",
        "datetime_created",
    )
    filter_horizontal: Tuple[str] = (
        "likes",
    )
    list_display: Tuple[str] = (
        "commentator",
        "news",
        "get_shorted_content",
        "get_is_deleted",
    )
    list_filter: Tuple[Any] = (
        CommonStateFilter,
    )
    search_fields: Tuple[str] = (
        "content",
    )
    save_on_top: bool = True

    def get_shorted_content(self, obj: Optional[Comment] = None) -> Optional[str]:  # noqa
        if obj:
            return f'{obj.content[:50]}...'
    get_shorted_content.short_description = "Контент комментария"

    def get_is_deleted(self, obj: Optional[Comment] = None) -> str:  # noqa
        if obj.datetime_deleted:
            return mark_safe(
                '<p style="color:red; font-weight:bold; font-size:17px; margin:0;">\
Комментарий удален</p>'
            )
        return mark_safe(
                '<p style="color:green; font-weight:bold;font-size:17px; margin:0;">\
Комментарий не удален</p>'
            )
    get_is_deleted.short_description = "Существование комментария"
    get_is_deleted.empty_value_display = "Комментарий не удален"
