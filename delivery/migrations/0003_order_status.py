# Generated by Django 4.0.3 on 2022-04-16 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_offer_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Создан'), (1, 'Обрабатывается'), (2, 'Сбор заказа'), (3, 'Передан в доставку'), (4, 'Доставлен'), (5, 'Отменен пользователем'), (6, 'Отменен оператором'), (7, 'Внутренняя ошибка сервиса'), (8, 'Не доставлено'), (9, 'Нет остатков')], default=0),
        ),
    ]