# Generated by Django 4.0.3 on 2022-04-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addition',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Дополнительно'),
        ),
    ]
