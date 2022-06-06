import uuid

from django.db import models


def carousel_directory_path(instance, filename):
    return 'carousel/img_{0}.{1}'.format(uuid.uuid4().hex, filename.split('.')[-1])


class CarouselPost(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=64
    )

    desc = models.CharField(
        verbose_name="Описание",
        max_length=128
    )

    img = models.ImageField(
        verbose_name="Изображение",
        upload_to=carousel_directory_path
    )

    class Meta:
        verbose_name = "Запись в карусели"
        verbose_name_plural = "Записи в карусели"
    
    def __str__(self) -> str:
        return self.title
