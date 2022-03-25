from django.urls import path #, include
from delivery.views import index as index_view
from delivery.views import DetailCart

urlpatterns = [
    path('', index_view, name='index'),
    path('cart/<int:pk>/', DetailCart.as_view(), name='detail-cart')
]