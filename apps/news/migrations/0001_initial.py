# Generated by Django 4.0.4 on 2022-06-04 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
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
                ('slug', models.SlugField(help_text='URL для поиска категории по его наименованию', max_length=100, unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('-datetime_updated',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(help_text='URL для поиска тэга по его наименованию', max_length=100, unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ('-datetime_updated',),
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
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='news', to='news.category', verbose_name='Категория')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='group_news', to='groups.group', verbose_name='Создано группой')),
                ('liked_users', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL, verbose_name='Лайки ползователей')),
                ('tags', models.ManyToManyField(blank=True, related_name='news', to='news.tag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ('datetime_updated',),
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
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='comments', to='news.news', verbose_name='Новость')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-datetime_updated',),
            },
        ),
    ]