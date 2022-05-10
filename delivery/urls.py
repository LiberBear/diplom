from django.urls import path, include

from rest_framework.routers import SimpleRouter

from delivery.views import IndexView, OffersView, CartView
from delivery.views import cart_manage, cart_checkout

urlpatterns = [
    # Common pages
    path('', IndexView.as_view(), name='index'),
    path('offers/', OffersView.as_view(), name='offers_page'),
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('cart/checkout', cart_checkout, name='cart_checkout'),
    path('cart/manage/', cart_manage, name='cart_manage'),
]
