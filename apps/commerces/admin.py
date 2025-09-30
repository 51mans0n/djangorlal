from django.contrib import admin
from .models import Address, PromoCode, Order, OrderItem, OrderItemOption, OrderPromo

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "label", "city")
    search_fields = ("user__username", "label", "city")

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "is_active")
    search_fields = ("code",)
    list_filter = ("is_active",)

class OrderItemOptionInline(admin.TabularInline):
    model = OrderItemOption
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "status", "total", "created_at")
    list_filter = ("status", "restaurant")
    search_fields = ("user__username", "restaurant__name")
    inlines = [OrderItemInline]

@admin.register(OrderPromo)
class OrderPromoAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "promo", "applied_amount")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "item_name", "unit_price", "qty", "line_total")
    inlines = [OrderItemOptionInline]
