import uuid

from django.db import models

from backend.base_models import BaseModel

from delivery.models.Measure import Measure


def offer_directory_path(instance, filename):
    return 'offers/img_{0}.{1}'.format(uuid.uuid4().hex, filename.split('.')[-1])


class OutOfStockException(Exception):
    pass


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
        upload_to=offer_directory_path
    )

    stock = models.PositiveBigIntegerField(
        verbose_name="Остатки",
        default=0
    )

    hidden = models.BooleanField(
        verbose_name="Скрыт",
        default=False
    )

    def increase_stock(self, count=1):
        self.stock = self.stock + count
        self.save()

    def decrease_stock(self, count=1):
        self.stock = self.stock - count
        self.save()

    def set_stock(self, val=0):
        self.stock = val
        self.save()

    def have_stock(self) -> bool:
        return self.stock > 0


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.title} {self.amount} {self.meas.title_short}'
