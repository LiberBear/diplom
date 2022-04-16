from pydoc import cram
from django.db import models

from backend.base_models import BaseModel
from delivery.models.Promo import Promo
from delivery.models.Cart import Cart


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

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.sum}'
    