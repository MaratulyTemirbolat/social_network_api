# Generated by Django 4.0.4 on 2022-06-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privilege',
            name='name_ru',
            field=models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Наименование на русском'),
        ),
    ]
