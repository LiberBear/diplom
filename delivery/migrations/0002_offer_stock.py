# Generated by Django 3.2.2 on 2022-04-04 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='stock',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Остатки'),
        ),
    ]