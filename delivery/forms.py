from django import forms
from django.core.validators import validate_integer
from django.core.validators import validate_integer

from delivery.models.Offer import Offer


class OfferForm(forms.ModelForm):
    """Форма для вывода информации об оффере"""
    class Meta:
        model = Offer
        fields = ["title", "desc", "img", "stock", "id"]


class AddToCartForm(forms.Form):
    """Форма добавления в корзину"""
    offer = forms.IntegerField(label="Товар")
    quantity = forms.IntegerField(label="Количество")