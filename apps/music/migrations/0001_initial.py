# Generated by Django 4.0.4 on 2022-05-25 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('music', models.FileField(unique=True, upload_to='documents/songs/%Y/%m/%d', verbose_name='Файл песни')),
                ('performers', models.ManyToManyField(related_name='performer_songs', to='music.performer', verbose_name='Певцы')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='playlist_songs', to='music.playlist', verbose_name='Плэйлист')),
                ('users', models.ManyToManyField(blank=True, related_name='user_songs', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
