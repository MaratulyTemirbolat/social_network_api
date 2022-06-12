# Generated by Django 4.0.4 on 2022-06-12 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_alter_city_options'),
        ('photos', '0002_profilephoto_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='profile_photos', to='locations.city', verbose_name='Город, где сделано фото'),
        ),
    ]
