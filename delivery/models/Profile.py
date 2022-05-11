from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from backend.base_models import BaseModel

from phonenumber_field.modelfields import PhoneNumberField

from account.signals import user_signed_up


class Profile(BaseModel):
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения',
    )
    address = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name='Адрес проживания',
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name='Номер телефона',
    )

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.email}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            instance.profile = Profile.objects.create(user=instance)

    @receiver(user_signed_up)
    def handle_user_signed_up(sender, user, form, **kwargs):
        profile = user.profile
        profile.save()
