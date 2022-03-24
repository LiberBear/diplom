from django.db import models
from django.contrib.auth.models import User
from backend.base_models import BaseModel
from delivery.models.Offer import Offer


class Cart(BaseModel):
    """Корзина"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="Пользователь",
        null=False,
        blank=False
    )

    def clear(self):
        """Удалить все товары из корзины пользователя"""
        items = CartItem.objects.filter(cart=self.id)
        if items.exists():
            items.all().delete()

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f'Корзина {self.user}'


class CartItem(BaseModel):
    """Позиция в корзине"""

    offer = models.OneToOneField(
        Offer,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="Товар",
        null=False,
        blank=False
    )
    
    cart = models.OneToOneField(
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
    


    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"

    def __str__(self):
        return f'{self.offer} - {self.quantity} шт. - {self.cart.user}'    
