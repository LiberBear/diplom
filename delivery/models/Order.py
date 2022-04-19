from django.db import models

from backend.base_models import BaseModel

from delivery.models.Promo import Promo
from delivery.models.Cart import Cart
from delivery.models.Address import Address


class OrderStatus(models.IntegerChoices):
    CREATED = 0, "Создан"
    PROCESSING = 1, "Обрабатывается"
    WAITING = 2, "Сбор заказа"
    DELIVERY = 3, "Передан в доставку"
    DONE = 4, "Доставлен",
    CANCELED_BY_USER = 5, "Отменен пользователем"
    CANCELED_BY_OPERATOR = 6, "Отменен оператором"
    ERROR_INTERNAL = 7, "Внутренняя ошибка сервиса",
    ERROR_DELIVERY = 8, "Не доставлено",
    ERROR_STOCK = 9, "Нет остатков",


class Order(BaseModel):

    items = models.JSONField(
        verbose_name="Товары (снимок)"
    )

    address = models.ForeignKey(
        Address,
        verbose_name="Адрес",
        on_delete=models.CASCADE
    )

    comment = models.CharField(
        max_length=512,
        verbose_name="Комментарий",
        blank=True,
        null=True
        )

    sum = models.DecimalField(
        verbose_name="Сумма",
        max_digits=15,
        decimal_places=2,
        default=0.0
    )

    promo = models.ForeignKey(
        Promo,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="Промокод",
        null=True,
        blank=True
        )

    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
        verbose_name="Статус заказа"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ {self.id} на основе {self.cart}'
    