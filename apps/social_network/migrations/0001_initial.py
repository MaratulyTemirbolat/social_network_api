# Generated by Django 4.0.4 on 2022-06-04 10:54

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
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, verbose_name='Наименованеи города')),
                ('is_capital', models.BooleanField(default=False, verbose_name='Столица')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Столицы',
                'ordering': ('-datetime_updated',),
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
                ('slug', models.SlugField(help_text='URL для поиска причина жалобы по её наименованию', max_length=100, unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Причина жалобы',
                'verbose_name_plural': 'Причины жалоб',
                'ordering': ('-datetime_updated',),
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
                ('slug', models.SlugField(help_text='URL для поиска страны по её названию', max_length=100, unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('-datetime_updated',),
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=250, verbose_name='Название видео')),
                ('video_file', models.FileField(upload_to='documents/videos/%Y/%m/%d', verbose_name='Видео файл')),
                ('keepers', models.ManyToManyField(related_name='added_videos', to=settings.AUTH_USER_MODEL, verbose_name='Имеется пользователями')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='owned_videos', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видосики',
                'ordering': ('-datetime_updated',),
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
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='profile_photos', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Фотография профиля',
                'verbose_name_plural': 'Фотографии профиля',
                'ordering': ('-datetime_updated',),
            },
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
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
                'ordering': ('-datetime_updated',),
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='attached_cities', to='social_network.country', verbose_name='Страна'),
        ),
    ]
