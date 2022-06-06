from django.db import models

from backend.base_models import BaseModel
from django.contrib.auth.models import User


class Address(BaseModel):
    """Модель адреса доставки"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    city = models.CharField(verbose_name="Город", max_length=32)
    street = models.CharField(verbose_name="Улица", max_length=64)
    house = models.IntegerField(verbose_name="Дом")
    apartment = models.IntegerField(verbose_name="Квартира")
    addition = models.CharField(verbose_name="Дополнительно", max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = "Aдрес"
        verbose_name_plural = "Aдреса"

    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.apartment}'

    @property
    def full_addr(self):
        return str(self)
