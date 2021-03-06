# Generated by Django 4.0.4 on 2022-07-11 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auths', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(max_length=100, verbose_name='Название группы')),
                ('slug', models.SlugField(help_text='URL для поиска группы (будет в нижнем регистре)', max_length=100, unique=True, verbose_name='URL (на группу)')),
                ('followers', models.ManyToManyField(blank=True, related_name='followed_groups', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики')),
            ],
            options={
                'verbose_name': 'Группа (Сообщество)',
                'verbose_name_plural': 'Группы (Сообщества)',
                'ordering': ('-datetime_updated',),
            },
        ),
        migrations.CreateModel(
            name='Privilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name_en', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Наименование на английском')),
                ('name_ru', models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Наименование на русском')),
                ('slug', models.SlugField(blank=True, help_text='URL для поиска привилегий по названию', unique=True, verbose_name='URL (shared link)')),
            ],
            options={
                'verbose_name': 'Привилегия (В группе)',
                'verbose_name_plural': 'Привилегии (В группах)',
                'ordering': ('-datetime_updated',),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(help_text='URL для поиска роли по наименованию', unique=True, verbose_name='Url')),
                ('privileges', models.ManyToManyField(related_name='positions', to='groups.privilege')),
            ],
            options={
                'verbose_name': 'Роль (в группе)',
                'verbose_name_plural': 'Роли (в группе)',
                'ordering': ('datetime_created',),
            },
        ),
        migrations.CreateModel(
            name='GroupAdministration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group', verbose_name='Группа')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.role', verbose_name='Роль')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь группы')),
            ],
            options={
                'verbose_name': 'Роль пользователя в группе',
                'verbose_name_plural': 'Роли пользователей в группах',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='group',
            name='members_rights',
            field=models.ManyToManyField(related_name='groups_rights', through='groups.GroupAdministration', to=settings.AUTH_USER_MODEL, verbose_name='Позиция в группе'),
        ),
        migrations.AddConstraint(
            model_name='groupadministration',
            constraint=models.UniqueConstraint(fields=('group', 'user', 'role'), name='unique_group_user_role'),
        ),
    ]
