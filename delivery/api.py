# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action

from delivery.serializers import OfferSerializer, CartItemSerializer, OrderSerializer

from delivery.models.Offer import Offer, OutOfStockException
from delivery.models.Cart import Cart, CartItem, TooBigCartException, TooLowCartException
from delivery.models.Order import Order


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class OffersViewSet(ModelViewSet):
    """API для получения всех товаров"""
    queryset = Offer.objects.filter(hidden=False).order_by("id")
    serializer_class = OfferSerializer
    # доступ к товарам только на чтение
    permission_classes = [ReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'desc']
    ordering_filters = ['title', 'price']


class CartViewSet(ModelViewSet):
    queryset = None
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['offer', 'desc']
    ordering_filters = ['created_at']

    @staticmethod
    def get_current_cart(request) -> Cart:
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        return cart

    def get_queryset(self):
        cart = self.get_current_cart(self.request)
        return CartItem.objects.filter(cart=cart)

    # вот тут дописать метода по редактированию корзинки
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        data = request.data
        serializer = CartItemSerializer(data=data)
        # Проверка пришедших данных
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        offer_id = data['offer']
        quantity = data['quantity']
        offer = get_object_or_404(Offer, pk=int(offer_id))
        stock = offer.stock
        if quantity <= 0:
            return Response({
                'status': 'error',
                'msg': 'Нельзя добавить в корзину количество равное нулю',
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > stock:
            return Response({
                'status': 'error',
                'msg': 'Данного товара нет в таком количество на складе'
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_current_cart(request)
        try:
            cart_item = CartItem.objects.get(cart=cart, offer=offer)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(offer=offer, cart=cart, quantity=0)

        try:
            cart_item.increase(amount=quantity)
            serializer = CartItemSerializer(cart_item)
            return Response({"status": "ok", "cart": serializer.data})
        except TooBigCartException:
            return Response({"status": "error", "msg": "Вы запросили в корзине больше товара, чем есть на складе"},
                            status=status.HTTP_400_BAD_REQUEST)
        except OutOfStockException:
            return Response({"status": "error", "msg": "Вы привысили наши остатки на складе"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def delete_item(self, request):
        data = request.data
        serializer = CartItemSerializer(data=data)
        # Проверка пришедших данных
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        offer_id = data['offer']
        quantity = data['quantity']
        offer = get_object_or_404(Offer, pk=int(offer_id))
        stock = offer.stock
        if quantity <= 0:
            return Response({
                'status': 'error',
                'msg': 'Нельзя убрать из корзины количество равное нулю',
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        cart = self.get_current_cart(request)

        try:
            cart_item = CartItem.objects.get(cart=cart, offer=offer)
        except CartItem.DoesNotExist:
            return Response({"status": "error", "msg": "В корзине нет указанной позиции"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item.decrease(amount=quantity)
            serializer = CartItemSerializer(cart_item)
            return Response({"status": "ok", "cart": serializer.data})
        except TooLowCartException:
            return Response(
                {"status": "error", "msg": "Вы запросили уменьшить количество позиции "
                                           "в корзине меньше заданного предела"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_current_cart(request)
        cart.clear()
        return Response({"status": "ok"})


class OrderViewSet(ViewSet):
    """Обработка заказов"""
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        cart = Cart.objects.get_object_or_404(user=user, ordered=False)
        orders = Order.objects.filter(cart=cart)
        serializer = OrderSerializer(orders)
        return Response(serializer.data)