# Generated by Django 4.0.3 on 2022-06-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselpost',
            name='desc',
            field=models.CharField(max_length=128, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='carouselpost',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Заголовок'),
        ),
    ]
