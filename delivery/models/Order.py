from django.db import models
from django.db.models.signals import pre_save
from django.utils.timezone import now
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


class OrderPaymentType(models.IntegerChoices):
    FIAT =0, "Наличные",
    CC_OFFLINE = 1, "Банковской картой курьеру",
    # CC_ONLINE = 2, "Банковской картой онлайн",
    # PAYMENT_GATEWAY = 3, "Платежный шлюз"


class Order(BaseModel):
    """Модель заказа"""

    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
        verbose_name="Корзина",
        primary_key=True
        )

    address = models.ForeignKey(
        Address,
        verbose_name="Адрес",
        on_delete=models.PROTECT
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

    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
        verbose_name="Статус заказа"
    )

    payment_type = models.IntegerField(
        choices=OrderPaymentType.choices,
        default=OrderPaymentType.FIAT,
        verbose_name="Тип оплаты"
    )

    delivery_date = models.DateField(
        verbose_name="Дата доставки",
        default=now
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ {self.cart.id}'

    def save(self, *args, **kwargs):
        self.cart.set_ordered()
        self.sum = self.cart.total_price
        super(Order, self).save(*args, **kwargs)


def order_pre_save(sender, instance: Order, *args, **kwargs):
    """Доп процедуры перед сохранением заказа"""
    cart = instance.cart
    cart.is_ordered = True  # устанавливаем флаг на корзину
    cart.recalc_total() # пересчет корзины


# def order_post_save(sender, instance: Order, *args, **kwargs):
#     """Доп процедуры после сохранения заказа"""
#     cart = instance.cart
#     cart.is_ordered = True #устанавливаем флаг на корзину
#     cart.save()


pre_save.connect(order_pre_save, sender=Order)
#post_save.connect(order_post_save, sender=Order)

