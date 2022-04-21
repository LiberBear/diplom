from django.urls import path, include

from rest_framework.routers import SimpleRouter

from delivery.views import index as index_view
from delivery.views import offers_page, cart_page


urlpatterns = [
    # Common pages
    path('', index_view, name='index'),
    path('offers/', offers_page, name='offers_page'),
    path('cart/', cart_page, name='detail-cart'),
    path('accounts/', include('django.contrib.auth.urls')),
]
