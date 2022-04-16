from django.urls import path, include

from rest_framework.routers import SimpleRouter

from delivery.views import index as index_view
from delivery.views import offers_page
from delivery.api import OffersViewSet, CartViewSet

router = SimpleRouter()
router.register(r'offers', OffersViewSet)
router.register(r'cart', CartViewSet, 'carts')

urlpatterns = [
    # Common pages
    path('', index_view, name='index'),
    path('offers/', offers_page, name='offers_page'),
    #path('cart/', DetailCart.as_view(), name='detail-cart'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # API
    path('api/', include(router.urls), name='api'),
]
