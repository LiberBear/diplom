from pydoc import cram
from django.db import models

from backend.base_models import BaseModel
from delivery.models.Promo import Promo
from delivery.models.Cart import Cart


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

    cart = models.ForeignKey(
        Cart,
        verbose_name="Корзина товаров",
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    comment = models.CharField(
        max_length=512,
        verbose_name="Комментарий",
        blank=True,
        null=True
        )

    amount = models.IntegerField(
        verbose_name="Количество",
        default=0
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
        default=OrderStatus.CREATED
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.sum}'
    