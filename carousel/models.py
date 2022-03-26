from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models

# Create your models here.

class CarouselPost(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=32
    )

    desc = models.CharField(
        verbose_name="Описание",
        max_length=64
    )

    img = models.ImageField(
        verbose_name="Изображение",
        upload_to="carousel"
    )

    class Meta:
        verbose_name = "Запись в карусели"
        verbose_name_plural = "Записи в карусели"
    
    def __str__(self) -> str:
        return self.title
