from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from apps.catalogs.models import Restaurant, MenuItem

User = settings.AUTH_USER_MODEL

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=100, blank=True)  # например, "Дом", "Офис"
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["user", "id"]

    def __str__(self):
        return f"{self.user} — {self.label or self.line1}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONFIRMED = "confirmed", "Confirmed"
        DELIVERING = "delivering", "Delivering"
        DONE = "done", "Done"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    discount_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    promo_codes = models.ManyToManyField(PromoCode, through="OrderPromo", blank=True, related_name="orders")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.user} — {self.restaurant}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name="order_items")

    # Снапшоты имени и цены на момент покупки:
    item_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    qty = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["order_id", "id"]

    def __str__(self):
        return f"{self.item_name} x{self.qty} (order {self.order_id})"


class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="selected_options")
    option_name = models.CharField(max_length=120)
    price_delta = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["order_item_id", "id"]

    def __str__(self):
        return f"{self.option_name} (+{self.price_delta})"


class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promo = models.ForeignKey(PromoCode, on_delete=models.PROTECT)
    applied_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = [("order", "promo")]
        ordering = ["order_id", "id"]

    def __str__(self):
        return f"{self.promo.code} for order {self.order_id}: {self.applied_amount}"
