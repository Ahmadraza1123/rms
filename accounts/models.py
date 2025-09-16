from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin/Owner'),
        ('manager', 'Manager'),
        ('waiter', 'Waiter'),
        ('cashier', 'Cashier'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')




