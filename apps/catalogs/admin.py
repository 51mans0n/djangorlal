from django.contrib import admin
from .models import Restaurant, Category, Option, MenuItem, ItemCategory, ItemOption

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

class ItemCategoryInline(admin.TabularInline):
    model = ItemCategory
    extra = 1

class ItemOptionInline(admin.TabularInline):
    model = ItemOption
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "restaurant", "base_price", "is_available")
    list_filter = ("restaurant", "is_available")
    search_fields = ("title", "restaurant__name")
    inlines = [ItemCategoryInline, ItemOptionInline]
