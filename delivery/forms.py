from django import forms

from delivery.models.Offer import Offer


class OfferForm(forms.ModelForm):
    """Форма для вывода информации об оффере"""
    class Meta:
        model = Offer
        fields = ["title", "desc", "img", "stock", "id"]


class AddToCartForm(forms.Form):
    """Форма добавления в корзину"""
    offer_id = forms.NumberInput(attrs={'type': 'hidden'})
    referer = forms.TextInput(attrs={'type': 'hidden'})
    quantity = forms.NumberInput(attrs={'type': 'hidden'})

