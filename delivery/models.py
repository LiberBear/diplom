from lib2to3.pytree import Base
from django.db import models
from django.contrib.auth.models import User
from backend.base_models import BaseModel


class Promo(BaseModel):
    code = models.CharField(
        max_length=16,
        verbose_name="Код",
        blank=False,
        null=False,
        unique=True
        )

    comment = models.CharField(
        max_length=64,
        verbose_name="Комментарий",
        blank=True,
        null=True
        )
        
    date_start = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=False,
        blank=False,
        verbose_name="Дата начала действия",
        )

    date_end = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=False,
        blank=False,
        verbose_name="Дата конца действия",
        )

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return f'[{self.code}] {self.date_start}--{self.date_end}'


class Measure(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name="Наименование",
        blank=False,
        null=False
        )

    title = models.CharField(
        max_length=8,
        verbose_name="Наименование (кратко)",
        blank=False,
        null=False
        ) 
              
    class Meta:
        verbose_name = "Измерение"
        verbose_name_plural = "Измерения"

    def __str__(self):
        return self.title


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
 
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=15,
        decimal_places=2,
        default=0.0
    )   

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return {self.title}


class Order(BaseModel):
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

    meas = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        default=0,
        verbose_name="В чем измеряется",
        null=False,
        blank=False
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
