# Generated by Django 3.2.2 on 2022-03-25 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.cart', verbose_name='Корзина пользователя'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='offer',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.offer', verbose_name='Товар'),
        ),
    ]