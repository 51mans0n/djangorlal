from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-date_joined",)
    list_display = ("email","first_name","last_name","role","department","city","country","is_active","is_staff","date_joined","last_login")
    search_fields = ("email","first_name","last_name","city","country","department")

    fieldsets = (
        (None, {"fields": ("email","password")}),
        ("Personal info", {"fields": ("username","first_name","last_name","phone","city","country","department","role","birth_date","salary")}),
        ("Permissions", {"fields": ("is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Important dates", {"fields": ("last_login","date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email","password1","password2","is_active","is_staff","is_superuser"),
        }),
    )

    def get_username(self, obj): 
        return obj.email
