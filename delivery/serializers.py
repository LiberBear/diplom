from rest_framework.serializers import ModelSerializer

from delivery.models.Offer import Offer
from delivery.models.Cart import Cart, CartItem


class OfferSerializer(ModelSerializer):
    """Оффер"""

    class Meta:
        model = Offer
        fields = "__all__"


class CartItemSerializer(ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"
