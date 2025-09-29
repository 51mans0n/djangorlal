from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from decouple import config
from datetime import datetime
from zoneinfo import ZoneInfo

# 1) Welcome page с 3 кнопками
def welcome(request: HttpRequest) -> HttpResponse:
    return render(request, "home/welcome.html")

# 2) /users — список карточек пользователей
def users_list(request: HttpRequest) -> HttpResponse:
    users = [
        {"full_name": "Alice Johnson", "age": 21},
        {"full_name": "Bob Smith", "age": 19},
        {"full_name": "Charlie Brown", "age": 25},
        {"full_name": "Dana White", "age": 23},
    ]
    return render(request, "home/users.html", {"users": users})

# 3) /city-time — текущее время выбранного города
def city_time(request: HttpRequest) -> HttpResponse:
    choices = {
        "Almaty": "Asia/Almaty",
        "Calgary": "America/Edmonton",
        "Moscow": "Europe/Moscow",
        "UTC": "UTC",
    }
    selected = request.GET.get("city", "Almaty")
    tzname = choices.get(selected, "Asia/Almaty")
    now = datetime.now(ZoneInfo(tzname))
    ctx = {
        "choices": list(choices.keys()),
        "selected": selected,
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render(request, "home/city_time.html", ctx)

# 4) /cnt — счётчик с увеличением и сбросом
def counter(request: HttpRequest) -> HttpResponse:
    count = request.session.get("count", 0)

    if request.method == "POST":
        if "inc" in request.POST:
            count += 1
        elif "reset" in request.POST:
            count = 0
        request.session["count"] = count
        return redirect("counter")

    return render(request, "home/counter.html", {"count": count})

# 5) /env — показать текущее окружение
def env_view(request: HttpRequest) -> HttpResponse:
    env_id = config("DJANGORLAR_ENV_ID", default="local")
    return render(request, "home/env.html", {"env_id": env_id})
