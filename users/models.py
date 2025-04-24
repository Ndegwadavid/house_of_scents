from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=[('customer', 'Customer'), ('admin', 'Admin')], default='customer')
    verification_token = models.CharField(max_length=36, blank=True, null=True)
    receive_stock_alerts = models.BooleanField(default=False)  # Opt-in for stock alerts

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email