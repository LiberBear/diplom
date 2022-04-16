from django.db import models
from django.contrib.auth.models import User
from backend.base_models import BaseModel
from delivery.models.Offer import Offer
from django.db.models import F, Sum


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
        items = CartItem.objects.filter(cart=self.id)
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
        return f'Корзина {self.user}'


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

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"

    def __str__(self):
        return f'{self.offer} - {self.quantity} шт. - {self.cart.user}'    
