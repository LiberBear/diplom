from django.urls import path #, include
from delivery.views import index as index_view
from delivery.views import DetailCart, offers_page

urlpatterns = [
    path('', index_view, name='index'),
    path('offers/', offers_page, name='offers_page'),
    path('cart/<int:pk>/', DetailCart.as_view(), name='detail-cart')
]