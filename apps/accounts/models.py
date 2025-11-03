from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin

class AppUser(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True)
    is_customer = models.BooleanField(default=True)

    class Meta:
        abstract = True   

    def __str__(self):
        return self.username

class EmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True  

    def __str__(self):
        return self.email
