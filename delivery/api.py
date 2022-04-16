from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from delivery.serializers import OfferSerializer, CartItemSerializer

from delivery.models.Offer import Offer
from delivery.models.Cart import Cart, CartItem


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class OffersViewSet(ModelViewSet):
    """API для получения всех товаров"""
    queryset = Offer.objects.all().order_by("id")
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'desc']
    ordering_filters = ['title']


class CartViewSet(ViewSet):
    """Текущая корзинка пользователя"""
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        user = request.user
        cart, cart_created = Cart.objects.get_or_create(user=user, ordered=False)
        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        print(serializer.data)
        return Response(serializer.data)
