from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    """ Базовая модель данных """

    created_at = models.DateTimeField(
        verbose_name="Дата добавления в БД",
        editable=False,
        default=now,
        blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения в БД",
        editable=False,
        blank=True,
        auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        #indexes = [models.Index(fields=['created_at', 'updated_at', ]), ]
