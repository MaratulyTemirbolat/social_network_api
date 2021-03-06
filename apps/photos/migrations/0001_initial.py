# Generated by Django 4.0.4 on 2022-07-11 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='время удаления')),
                ('photo', models.ImageField(upload_to='photos/profile_photos/%Y/%m/%d', verbose_name='Фото профиля')),
                ('description', models.TextField(blank=True, verbose_name='Описание фото')),
                ('likes_number', models.IntegerField(default=0, verbose_name='Количество лайков')),
                ('is_title', models.BooleanField(default=False, verbose_name='Аватарка')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_photos', to='locations.city', verbose_name='Город, где сделано фото')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_photos', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Фотография профиля',
                'verbose_name_plural': 'Фотографии профиля',
                'ordering': ('-datetime_updated',),
            },
        ),
    ]
