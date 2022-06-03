from django import forms

from delivery.models import Address
from delivery.models.Offer import Offer
from delivery.models.Order import Order, OrderPaymentType


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
    def __init__(self, user, *args, **kwargs):
        super(CartCheckoutForm, self).__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)

    address = forms.ModelChoiceField(
        label="Адрес доставки",
        queryset=Address.objects.filter(user__id=0),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    payment_type = forms.ChoiceField(
        label="Тип оплаты",
        choices=OrderPaymentType.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    comment = forms.CharField(
        label="Комментарий к заказу",
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )
    delivery_date = forms.DateField(
        label="Предпочтительная дата доставки",
        required=True,
        widget=forms.DateInput(attrs={
            'id': 'date_picker',
            'class': 'form-control',
            'type': 'date'
        }),
    )
