from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.db.transaction import atomic

from backend.base_models import BaseModel
from delivery.models.Offer import Offer, OutOfStockException


class TooBigCartException(Exception):
    pass


class TooLowCartException(Exception):
    pass


class Cart(BaseModel):
    """Корзина"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="Пользователь",
        null=False,
        blank=False
    )

    ordered = models.BooleanField(
        verbose_name="Есть в заказе?",
        default=False
    )

    def clear(self):
        """Удалить все товары из корзины пользователя"""
        items = CartItem.objects.filter(cart=self)
        if items.exists():
            items.all().delete()

    @property
    def total(self):
        """Получить полную стоимость корзины"""
        cart_items = CartItem.objects.filter(cart=self.id).prefetch_related("offer")
        annotation = cart_items.annotate(total_item=F('quantity')*F('offer__price'))
        aggregation = annotation.aggregate(total_cart=Sum('total_item'))
        total = aggregation.get('total_cart')
        return total

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f'Корзина №{self.id} пользователя {self.user}'


class CartItem(BaseModel):
    """Позиция в корзине"""

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="Товар",
        null=False,
        blank=False
    )
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="Корзина пользователя",
        null=False,
        blank=False       
    )

    quantity = models.IntegerField(
        verbose_name="Количество",
        default=1,
    )

    @property
    def total(self):
        """Получить полную стоимость позиции"""
        return self.offer.price * self.quantity

    @atomic
    def increase(self, amount: int = 1):
        """Увеличение количества товара в коризне с проверкой """
        stock = self.offer.stock
        total_quantity = self.quantity + amount
        if stock == 0:
            raise OutOfStockException()

        if total_quantity > stock:
            raise TooBigCartException()

        self.quantity = self.quantity + amount
        self.save()

    @atomic
    def decrease(self, amount: int = 1):
        """Уменьшение количества товара в коризне с проверкой """
        if amount > self.quantity:
            raise TooLowCartException()

        self.quantity = self.quantity - amount
        self.save()

    @atomic
    def set(self, amount: int):
        """Установка количества товара в коризне без проверки"""
        self.quantity = amount
        self.save()

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"

    def __str__(self):
        return f'{self.offer} - {self.quantity} шт. - {self.cart.user}'    
