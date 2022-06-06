from django.contrib import admin
from delivery.models import (Offer,
                             Order,
                             Measure,
                             Cart,
                             Address,
                             Profile
                             )
from delivery.models.Cart import CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Поля для отображения
    list_display = ("address", "user_info", "quantity_info", "sum", "payment_type","created_at", "delivery_date")
    # Поля для фильтрации
    list_filter = ("status", "payment_type", "created_at", "delivery_date")
    # Поля для поиска
    search_fields = ("cart__user__username", "address__full_addr")
    # Поля только для чтения
    readonly_fields = ('cart', 'sum', 'created_at', 'updated_at')
    # Запросы для отображения связанных сущностей
    @admin.display(description="Пользователь")
    def user_info(self, object):
        return f'{object.cart.user.last_name} {object.cart.user.first_name}'
    @admin.display(description="Количество позиций")
    def quantity_info(self, object):
        return str(object.cart.items_count)


admin.site.register(Offer)
admin.site.register(Measure)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Profile)
