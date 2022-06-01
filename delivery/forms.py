from django import forms
from django.core.validators import validate_integer
from django.core.validators import validate_integer

from delivery.models.Offer import Offer
from delivery.models.Order import Order, OrderPaymentType
from delivery.models.Address import Address
from delivery.models.Cart import Cart


class OfferForm(forms.ModelForm):
    """Форма для вывода информации об оффере"""

    class Meta:
        model = Offer
        fields = ["title", "desc", "img", "stock", "id"]


class AddToCartForm(forms.Form):
    """Форма добавления в корзину"""
    offer = forms.IntegerField(label="Товар")
    quantity = forms.IntegerField(label="Количество")


class CartCheckoutForm(forms.Form):
    """Форма оформления заказа"""
    city = forms.CharField(
        label="Город",
        required=True,
        initial="Чебоксары",
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    street = forms.CharField(
        label="Улица",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    house = forms.CharField(
        label="Дом",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    payment_type = forms.ChoiceField(
        label="Тип оплаты",
        choices=OrderPaymentType.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    delivery_date = forms.DateField(
        label="Дата доставки",
        required=True,
        widget=forms.DateInput(attrs={
            'id': 'date_picker',
            'class': 'form-control',
            'type': 'date'
        }),
    )
