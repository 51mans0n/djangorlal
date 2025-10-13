from apps.abstracts.models import AbstractSoftDeletableModel
from django.db import models
from apps.abstracts.models import AbstractSoftDeletableModel
from django.core.validators import MinValueValidator

class Restaurant(AbstractSoftDeletableModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(AbstractSoftDeletableModel):
    title = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Option(AbstractSoftDeletableModel):
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = [("name",)]
        ordering = ["name"]

    def __str__(self):
        return self.name


class MenuItem(AbstractSoftDeletableModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

    categories = models.ManyToManyField(
        Category,
        through="ItemCategory",
        related_name="menu_items",
        blank=True,
    )
    options = models.ManyToManyField(
        Option,
        through="ItemOption",
        related_name="menu_items",
        blank=True,
    )

    class Meta:
        unique_together = [("restaurant", "title")]
        ordering = ["restaurant__name", "title"]

    def __str__(self):
        return f"{self.title} ({self.restaurant})"


class ItemCategory(AbstractSoftDeletableModel):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = [("menu_item", "category")]
        ordering = ["menu_item_id", "position"]

    def __str__(self):
        return f"{self.menu_item} in {self.category} #{self.position}"


class ItemOption(AbstractSoftDeletableModel):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = [("menu_item", "option")]
        ordering = ["menu_item_id", "option_id"]

    def __str__(self):
        return f"{self.option} for {self.menu_item} (+{self.price_delta})"
