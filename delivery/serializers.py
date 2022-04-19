from rest_framework.serializers import ModelSerializer, StringRelatedField

from delivery.models.Offer import Offer
from delivery.models.Cart import Cart, CartItem
from delivery.models.Order import Order
from delivery.models.Measure import Measure


class MeasSerializer(ModelSerializer):

    class Meta:
        model = Measure
        fields = ['title', 'title_short']


class OfferSerializer(ModelSerializer):
    meas = MeasSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'desc',
            'amount',
            'price',
            'img',
            'stock',
            'meas'
        ]


class CartItemSerializer(ModelSerializer):

    class Meta:
        model = CartItem
        fields = [
            'offer',
            'quantity'
        ]
        extra_kwargs = {
            'offer': {'required': True},
            'quantity': {'required': True},
        }


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"