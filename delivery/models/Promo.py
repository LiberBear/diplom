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