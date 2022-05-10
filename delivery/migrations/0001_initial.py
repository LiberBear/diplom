# Generated by Django 4.0.3 on 2022-05-10 16:22

import delivery.models.Offer
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields

from delivery.models.Offer import offer_directory_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('city', models.CharField(max_length=32, verbose_name='Город')),
                ('street', models.CharField(max_length=64, verbose_name='Улица')),
                ('house', models.IntegerField(verbose_name='Дом')),
                ('apartment', models.IntegerField(verbose_name='Квартира')),
                ('addition', models.CharField(blank=True, max_length=64, null=True, verbose_name='Дополнительно')),
            ],
            options={
                'verbose_name': 'Aдрес',
                'verbose_name_plural': 'Aдреса',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('ordered', models.BooleanField(default=False, verbose_name='Есть в заказе?')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Общая сумма корзины')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('title', models.CharField(max_length=128, verbose_name='Наименование')),
                ('title_short', models.CharField(max_length=8, verbose_name='Наименование (кратко)')),
            ],
            options={
                'verbose_name': 'Измерение',
                'verbose_name_plural': 'Измерения',
            },
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('code', models.CharField(max_length=16, unique=True, verbose_name='Код')),
                ('comment', models.CharField(blank=True, max_length=64, null=True, verbose_name='Комментарий')),
                ('date_start', models.DateField(verbose_name='Дата начала действия')),
                ('date_end', models.DateField(verbose_name='Дата конца действия')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('address', models.CharField(max_length=500, verbose_name='Адрес проживания')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('title', models.CharField(max_length=128, verbose_name='Наименование')),
                ('desc', models.CharField(max_length=512, verbose_name='Описание')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Количество/Обьем')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Цена')),
                ('img', models.ImageField(upload_to=offer_directory_path, verbose_name='Изображение')),
                ('stock', models.PositiveBigIntegerField(default=0, verbose_name='Остатки')),
                ('hidden', models.BooleanField(default=False, verbose_name='Скрыт')),
                ('meas', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.measure', verbose_name='В чем измеряется')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('cart', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.cart', verbose_name='Корзина пользователя')),
                ('offer', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.offer', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Позиция в корзине',
                'verbose_name_plural': 'Позиции в корзине',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата добавления в БД')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения в БД')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='delivery.cart', verbose_name='Корзина')),
                ('comment', models.CharField(blank=True, max_length=512, null=True, verbose_name='Комментарий')),
                ('sum', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Сумма')),
                ('status', models.IntegerField(choices=[(0, 'Создан'), (1, 'Обрабатывается'), (2, 'Сбор заказа'), (3, 'Передан в доставку'), (4, 'Доставлен'), (5, 'Отменен пользователем'), (6, 'Отменен оператором'), (7, 'Внутренняя ошибка сервиса'), (8, 'Не доставлено'), (9, 'Нет остатков')], default=0, verbose_name='Статус заказа')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.address', verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
