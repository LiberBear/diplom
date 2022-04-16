from tabnanny import verbose
from django.db import models

from backend.base_models import BaseModel
from delivery.models.Measure import Measure 


class Offer(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name="Наименование",
        blank=False,
        null=False
        )    

    desc = models.CharField(
        max_length=512,
        verbose_name="Описание",
        blank=False,
        null=False
        ) 
     
    meas = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="В чем измеряется",
        null=False,
        blank=False
    )

    amount = models.DecimalField(
        verbose_name="Количество/Обьем",
        max_digits=15,
        decimal_places=2,
        default=0.0
    )  

    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=15,
        decimal_places=2,
        default=0.0
    )   

    img = models.ImageField(
        verbose_name="Изображение",
        upload_to="offers"
    )

    stock = models.PositiveBigIntegerField(
        verbose_name="Остатки",
        default=0
    )

    def stock_increase(self, count=1):
        self.stock = self.stock + count
        self.save()

    def stock_decrease(self, count=1):
        self.stock = self.stock - count
        self.save()

    def stock_set(self, val=0):
        self.stock = val
        self.save()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.title} {self.amount} {self.meas.title_short}'
