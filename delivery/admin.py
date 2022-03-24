from django.contrib import admin
from delivery.models import (Promo,
                            Offer,
                            Order,
                            Measure)
# Register your models here.
admin.site.register(Promo)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Measure)
