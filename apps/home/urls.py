from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("users", views.users_list, name="users_list"),
    path("city-time", views.city_time, name="city_time"),
    path("cnt", views.counter, name="counter"),
    path("env", views.env_view, name="env_view"),
]
