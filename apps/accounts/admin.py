# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import AppUser, EmailUser

# @admin.register(AppUser)
# class AppUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (("Extra", {"fields": ("middle_name","is_customer")}),)
#     list_display = ("username","email","first_name","last_name","is_customer","is_staff")

# @admin.register(EmailUser)
# class EmailUserAdmin(admin.ModelAdmin):
#     list_display = ("email","full_name","is_active","is_staff","date_joined")
#     search_fields = ("email","full_name")