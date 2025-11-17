from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from faker import Faker
from random import choice, randint
from datetime import date
from decimal import Decimal

from apps.accounts.models import User

DEPARTMENTS = ["IT","HR","Sales","Finance"]
ROLES = ["admin","manager","employee"]

class Command(BaseCommand):
    help = "Generate 10,000 users using Faker in batches with bulk_create"

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=10000)
        parser.add_argument("--batch", type=int, default=1000)

    def handle(self, *args, **opts):
        total = opts["total"]
        batch_size = opts["batch"]

        fake = Faker(["en_US","ru_RU"])
        password_hash = make_password("12345")  

        users_to_create = []
        created = 0

        for i in range(total):
            first = fake.first_name()
            last  = fake.last_name()
            email = fake.unique.email()

            year = randint(1975, 2005)
            month = randint(1, 12)
            day = randint(1, 28)
            bdate = date(year, month, day)

            u = User(
                email=email,
                username=fake.user_name(),
                first_name=first,
                last_name=last,
                phone=fake.phone_number(),
                city=fake.city(),
                country=fake.country(),
                department=choice(DEPARTMENTS),
                role=choice(ROLES),
                birth_date=bdate,
                salary=Decimal(randint(200_000, 900_000)),
                is_active=True,
                is_staff=choice([True, False, False]),  
                date_joined=fake.date_time_between(start_date="-2y", end_date="now", tzinfo=timezone.get_current_timezone()),
                password=password_hash,
            )
            users_to_create.append(u)

            if len(users_to_create) >= batch_size:
                User.objects.bulk_create(users_to_create, batch_size=batch_size)
                created += len(users_to_create)
                self.stdout.write(self.style.SUCCESS(f"Inserted: {created}/{total}"))
                users_to_create = []

        if users_to_create:
            User.objects.bulk_create(users_to_create, batch_size=batch_size)
            created += len(users_to_create)

        self.stdout.write(self.style.SUCCESS(f"DONE. Total inserted: {created}"))
