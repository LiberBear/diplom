from django.urls import path

from delivery.views import IndexView, OffersView, CartView, ProfileView, CartCheckoutView
from delivery.views import cart_manage

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('offers/', OffersView.as_view(), name='offers_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # Корзина
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('cart/checkout', CartCheckoutView.as_view(), name='cart_checkout'),
    path('cart/manage/', cart_manage, name='cart_manage'),
]
