from django.db import models
from django.db.models import F, Sum
from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.contrib.auth.models import User

from backend.base_models import BaseModel

from delivery.models.Offer import Offer, OutOfStockException


class TooBigCartException(Exception):
    def __str__(self):
        return 'Вы добавили в корзину товара больше чем есть в наличии'


class TooLowCartException(Exception):
    def __str__(self):
        return 'Вы попытались уменьшить количество позиции на число превышающее его текущее количество у вас в корзине'


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

    total_price = models.DecimalField(
        default=0.0,
        max_digits=15,
        decimal_places=2,
        verbose_name="Общая сумма корзины"
    )

    def clear(self):
        """Удалить все товары из корзины пользователя"""
        items = CartItem.objects.filter(cart=self)
        if items.exists():
            items.all().delete()

    @property
    def items_count(self):
        """Получить количество позиций в корзине"""
        cart_items = CartItem.objects.filter(cart=self.id).prefetch_related("offer")
        return cart_items.count()

    @atomic
    def recalc_total(self):
        """Пересчитать полную стоимость корзины"""
        cart_items = CartItem.objects.filter(cart=self.id).prefetch_related("offer")
        if not cart_items.exists():
            self.total_price = 0.0
            self.save()
        else:
            annotation = cart_items.annotate(total_item=F('quantity')*F('offer__price'))
            aggregation = annotation.aggregate(total_cart=Sum('total_item'))
            self.total_price = aggregation.get('total_cart', 0.0)
            self.save()

    @atomic
    def set_ordered(self):
        self.recalc_total()
        cart_items = CartItem.objects.filter(cart=self.id).prefetch_related("offer")
        print(cart_items)
        for cart_item in cart_items:
            cart_item.offer.decrease_stock(cart_item.quantity)
        self.ordered = True
        self.save()

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
        default=0,
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


def after_cart_item_save(sender, instance: CartItem, *args, **kwargs):
    "Доп. процедуры после изменения состояния позиции в корзине"
    instance.cart.recalc_total()


post_save.connect(after_cart_item_save, sender=CartItem)
