from django.db import models

from backend.base_models import BaseModel


class Address(BaseModel):
    """Модель адреса доставки"""

    city = models.CharField(
        max_length=32,
        verbose_name="Город"
    )

    street = models.CharField(
        max_length=64,
        verbose_name="Улица"
    )

    house = models.IntegerField(
        verbose_name="Дом"
    )

    apartment = models.IntegerField(
        verbose_name="Квартира"
    )

    addition = models.CharField(
        max_length=64,
        verbose_name="Дополнительно",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Aдрес"
        verbose_name_plural = "Aдреса"

    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.apartment}'
