from django.db import models 

from django.db.models import (
    Q, Count, Avg, Max, Min, Sum, F, Value,
    Case, When, CharField, IntegerField, DecimalField
)
from django.db.models.functions import Concat, ExtractYear, ExtractMonth, Now
from datetime import timedelta, date
from django.utils import timezone
from apps.accounts.models import User


# 2.1
q_21 = User.objects.filter(is_active=True)

# 2.2
q_22 = User.objects.filter(email__iendswith="@gmail.com")

# 2.3
q_23 = User.objects.filter(city="Almaty")

# 2.4
q_24 = User.objects.exclude(city="Almaty")

# 2.5
q_25 = User.objects.filter(salary__gt=500_000)

# 2.6
q_26 = User.objects.filter(department="IT", country="Kazakhstan")

# 2.7
q_27 = User.objects.filter(birth_date__isnull=True)

# 2.8
q_28 = User.objects.filter(first_name__istartswith="A")

# 2.9
q_29 = User.objects.count()

# 2.10
q_210 = User.objects.order_by("-date_joined")[:20]

# 2.11
q_211 = User.objects.values_list("city", flat=True).distinct()

# 2.12
q_212 = User.objects.filter(department="Sales").count()

# 2.13
seven_days_ago = timezone.now() - timedelta(days=7)
q_213 = User.objects.filter(last_login__gte=seven_days_ago)

# 2.14
q_214 = User.objects.filter(Q(first_name__icontains="bek") | Q(last_name__icontains="bek"))

# 2.15
q_215 = User.objects.filter(salary__gte=300_000, salary__lte=700_000)

# 2.16
q_216 = User.objects.filter(department__in=["IT","HR","Finance"])

# 2.17
q_217 = User.objects.values("department").annotate(cnt=Count("id"))

# 2.18
q_218 = User.objects.values("department").annotate(cnt=Count("id")).order_by("-cnt")

# 2.19
q_219 = User.objects.values("city").annotate(cnt=Count("id")).order_by("-cnt")[:5]

# 2.20
q_220 = User.objects.filter(last_login__isnull=True)

# 2.21
q_221 = User.objects.aggregate(avg_salary=Avg("salary"))

# 2.22
q_222 = User.objects.aggregate(max_salary=Max("salary"), min_salary=Min("salary"))

# 2.23
q_223 = User.objects.filter(phone__contains="+7")

# 2.24
q_224 = User.objects.annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))

# 2.25
q_225 = User.objects.annotate(birth_year=ExtractYear("birth_date")).order_by("birth_year")

# 2.26
q_226 = User.objects.filter(birth_date__month=5)

# 2.27
q_227 = User.objects.filter(role="manager", salary__gt=400_000)

# 2.28
q_228 = User.objects.filter(Q(role="employee") | Q(department="HR"))

# 2.29
q_229 = User.objects.filter(is_active=True).values("city").annotate(cnt=Count("id"))

# 2.30
q_230 = User.objects.order_by("date_joined")[:10]

# 2.31
q_231 = User.objects.filter(city__istartswith="A", salary__gt=300_000)

# 2.32
q_232 = User.objects.filter(Q(department__isnull=True) | Q(department=""))

# 2.33
q_233 = User.objects.values("country").annotate(cnt=Count("id"), avg_salary=Avg("salary"))

# 2.34
q_234 = User.objects.filter(is_staff=True).order_by("-last_login")

# 2.35
q_235 = User.objects.exclude(email__icontains="example.com")

# 2.36 (через подзапрос средней)
avg_sal = User.objects.aggregate(a=Avg("salary"))["a"]
q_236 = User.objects.filter(salary__gt=avg_sal)

# 2.37
q_237 = User.objects.values("email").annotate(cnt=Count("id")).filter(cnt__gt=1)

# 2.38
q_238 = User.objects.annotate(
    salary_level=Case(
        When(salary__lt=300_000, then=Value("low")),
        When(salary__lte=700_000, then=Value("medium")),
        default=Value("high"),
        output_field=CharField()
    )
).order_by("salary_level")

# 2.39
year_start = date.today().replace(month=1, day=1)
q_239 = User.objects.filter(date_joined__date__gte=year_start)

# 2.40
q_240 = User.objects.values("department").annotate(payroll=Sum("salary")).order_by("-payroll")

# 2.41
q_241 = User.objects.filter(department="IT", last_login__isnull=True)

# 2.42
q_242 = User.objects.filter(country="Kazakhstan").filter(Q(city__isnull=True) | Q(city=""))

# 2.43
q_243 = User.objects.filter(birth_date__lt=date(1990,1,1), salary__isnull=False)

# 2.44
q_244 = User.objects.annotate(
    years_since_joined=(Now() - F("date_joined"))
)

# 2.45
q_245 = User.objects.filter(department="Sales", email__iendswith="@gmail.com", salary__gt=350_000)

# 2.46
q_246 = User.objects.order_by("country", "-salary")

# 2.47
q_247 = User.objects.values("role").annotate(cnt=Count("id")).filter(cnt__gt=100)

# 2.48
q_248 = User.objects.filter(last_login__lt=F("date_joined"))

# 2.49
q_249 = User.objects.annotate(
    is_senior=Case(
        When(birth_date__lt=date(1985,1,1), then=Value(True)),
        default=Value(False),
        output_field=models.BooleanField()
    )
)

# 2.50
q_250 = User.objects.values("department").annotate(
    avg_salary=Avg("salary"),
    cnt=Count("id")
).filter(cnt__gte=20).order_by("-avg_salary")

print("Users total:", q_29)
print("Avg salary:", q_221)
print("Departments:", list(q_217))
