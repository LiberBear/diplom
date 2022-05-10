from django.contrib import admin
from delivery.models import (Promo,
                             Offer,
                             Order,
                             Measure,
                             Cart,
                             Address,
                             Profile
                             )
from delivery.models.Cart import CartItem
# Register your models here.
admin.site.register(Promo)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Measure)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Profile)
