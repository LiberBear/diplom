from django.db import models
from backend.base_models import BaseModel

class Measure(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name="Наименование",
        blank=False,
        null=False
        )

    title_short = models.CharField(
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
