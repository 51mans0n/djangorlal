from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
import random

from apps.catalogs.models import Restaurant, MenuItem, Option
from apps.commerces.models import (
    Address, Order, OrderItem, OrderItemOption, PromoCode, OrderPromo
)

User = get_user_model()

class Command(BaseCommand):
    help = "Generate ~20 promo codes, ~20 addresses и ~20 orders (с позициями/опциями) для блока commerces"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # 1) пользователь
        user, _ = User.objects.get_or_create(
            username="demo", defaults={"email": "demo@example.com"}
        )

        # 2) промо-коды (20)
        promos = []
        for i in range(20):
            pc, _ = PromoCode.objects.get_or_create(code=f"SALE{i}", defaults={
                "description": "Auto", "is_active": True
            })
            promos.append(pc)

        # 3) адреса (20)
        addresses = []
        for i in range(20):
            addr = Address.objects.create(
                user=user,
                label=f"Addr {i}",
                line1=f"Street {i}",
                city="Almaty"
            )
            addresses.append(addr)

        # 4) заказы (20) + позиции и опции
        if not Restaurant.objects.exists() or not MenuItem.objects.exists():
            self.stdout.write(self.style.ERROR(
                "Нужны данные в catalogs: Restaurants и MenuItems. Заполни их сначала."
            ))
            return

        all_restos = list(Restaurant.objects.all())
        all_items  = list(MenuItem.objects.all())
        all_opts   = list(Option.objects.all()) or [None]

        created_orders = 0
        for i in range(20):
            rest = random.choice(all_restos)
            addr = random.choice(addresses)

            order = Order.objects.create(
                user=user,
                restaurant=rest,
                address=addr,
                status=random.choice([c[0] for c in Order.Status.choices]),
                subtotal=Decimal("0.00"),
                discount_total=Decimal("0.00"),
                total=Decimal("0.00"),
            )

            subtotal = Decimal("0.00")

            # 2-3 позиции в заказ
            for _ in range(random.randint(2, 3)):
                base = random.choice(all_items)
                unit_price = base.base_price
                qty = random.randint(1, 3)

                oi = OrderItem.objects.create(
                    order=order,
                    menu_item=base,
                    item_name=base.title,   # snapshot
                    unit_price=unit_price,  # snapshot
                    qty=qty,
                    line_total=Decimal("0.00"),  # временно, посчитаем ниже
                )

                # 0-2 опции на позицию
                delta_sum = Decimal("0.00")
                for opt in random.sample(all_opts, k=min(2, len(all_opts))):
                    if opt is None:
                        continue
                    delta = Decimal(random.randint(0, 400)) / 100  # 0.00..4.00
                    OrderItemOption.objects.create(
                        order_item=oi,
                        option_name=opt.name,     # snapshot
                        price_delta=delta,
                    )
                    delta_sum += delta

                oi.line_total = (unit_price + delta_sum) * qty
                oi.save(update_fields=["line_total"])
                subtotal += oi.line_total

            # промо на заказ (иногда)
            if random.choice([True, False]) and promos:
                disc = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))
                promo = random.choice(promos)
                OrderPromo.objects.create(order=order, promo=promo, applied_amount=disc)
                order.discount_total = disc

            order.subtotal = subtotal
            order.total = (subtotal - order.discount_total).quantize(Decimal("0.01"))
            order.save(update_fields=["subtotal", "discount_total", "total"])
            created_orders += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: {len(promos)} промо, {len(addresses)} адресов, {created_orders} заказов."
        ))
