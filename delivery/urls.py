from django.urls import path

from delivery.views import IndexView, OffersView, CartView, ProfileView, CartCheckoutView
from delivery.views import AddressListView, AddressUpdateView, AddressDeleteView, AddressCreateView
from delivery.views import cart_manage
from delivery.views import OrderSuccessView
from delivery.views import SettingsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('offers/', OffersView.as_view(), name='offers_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', SettingsView.as_view(), name='profile_settings'),
    # Адреса
    path('profile/address/', AddressListView.as_view(), name='address_list'),
    path('profile/address/create/', AddressCreateView.as_view(), name='address_create'),
    path('profile/address/update/<int:pk>/', AddressUpdateView.as_view(), name='address_update'),
    path('profile/address/delete/<int:pk>/', AddressDeleteView.as_view(), name='address_delete'),
    # Корзина
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('cart/checkout/', CartCheckoutView.as_view(), name='cart_checkout'),
    path('cart/manage/', cart_manage, name='cart_manage'),
    # Заказ
    path('order/success/<int:pk>/', OrderSuccessView.as_view(), name='order_success'),

]

