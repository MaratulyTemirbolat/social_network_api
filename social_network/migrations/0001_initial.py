# Generated by Django 4.0.4 on 2022-05-22 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auths', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('is_group', models.BooleanField(default=False, verbose_name='Группа')),
                ('photo', models.ImageField(blank=True, upload_to='photos/chats/%Y/%m/%d/', verbose_name='Миниатюра')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'ordering': ['-datetime_updated'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, verbose_name='Наименованеи города')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComplainReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название страны')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, verbose_name='Название группы')),
                ('followers', models.ManyToManyField(blank=True, related_name='followed_groups', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Никнейм')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('video_file', models.FileField(upload_to='documents/videos/%Y/%m/%d', verbose_name='Видео файл')),
                ('keepers', models.ManyToManyField(related_name='added_videos', to=settings.AUTH_USER_MODEL, verbose_name='Имеется пользователями')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='owned_videos', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('photo', models.ImageField(upload_to='photos/profile_photos/%Y/%m/%d', verbose_name='Фото профиля')),
                ('likes_number', models.IntegerField(default=0, verbose_name='Количество лайков')),
                ('is_title', models.BooleanField(default=False, verbose_name='Аватарка')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='profile_photos', to='social_network.city', verbose_name='Город, где сделано фото')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='profile_photos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
                ('privileges', models.ManyToManyField(related_name='positions', to='social_network.privilege')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=150, verbose_name='Название плэйлиста')),
                ('photo', models.ImageField(blank=True, upload_to='photos/playlists/%Y/%m/%d', verbose_name='Фото плэйлиста')),
                ('listeners', models.ManyToManyField(blank=True, related_name='playlists', to=settings.AUTH_USER_MODEL, verbose_name='Слушатели')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='phones', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('photo', models.ImageField(upload_to='photos/news/%Y/%m/%d', verbose_name='Миниатюра')),
                ('content', models.TextField(verbose_name='Контент новости')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='published_news', to=settings.AUTH_USER_MODEL, verbose_name='Автор новости')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='news', to='social_network.category', verbose_name='Категория')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='group_news', to='social_network.group', verbose_name='Создано группой')),
                ('liked_users', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL, verbose_name='Лайки ползователей')),
                ('tags', models.ManyToManyField(blank=True, related_name='news', to='social_network.tag', verbose_name='Тэги')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('music', models.FileField(unique=True, upload_to='documents/songs/%Y/%m/%d', verbose_name='Файл песни')),
                ('performers', models.ManyToManyField(related_name='performer_songs', to='social_network.performer', verbose_name='Певцы')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='playlist_songs', to='social_network.playlist', verbose_name='Плэйлист')),
                ('users', models.ManyToManyField(blank=True, related_name='user_songs', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('content', models.TextField(verbose_name='Конент')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='messages', to='social_network.chat', verbose_name='Чат')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-datetime_created'],
            },
        ),
        migrations.CreateModel(
            name='GroupAdministration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='social_network.group', verbose_name='Группа')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='social_network.position', verbose_name='Статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь группы')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='members_rights',
            field=models.ManyToManyField(related_name='groups_rights', through='social_network.GroupAdministration', to=settings.AUTH_USER_MODEL, verbose_name='Позиция в группе'),
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('content', models.TextField(verbose_name='Текст')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='complains', to=settings.AUTH_USER_MODEL, verbose_name='Владелец жалобы')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='complains', to='social_network.complainreason', verbose_name='Причина жалобы')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('content', models.TextField(verbose_name='Контент')),
                ('commentator', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Владелец комментария')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL, verbose_name='Лайки пользователей')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='comments', to='social_network.news', verbose_name='Новость')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='attached_cities', to='social_network.country', verbose_name='Страна'),
        ),
        migrations.CreateModel(
            name='ChatMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_name', models.CharField(default='Unkown', max_length=150, verbose_name='Никнейм в чате')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='social_network.chat', verbose_name='Чат')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='joined_chats', through='social_network.ChatMember', to=settings.AUTH_USER_MODEL, verbose_name='Члены чата'),
        ),
    ]
