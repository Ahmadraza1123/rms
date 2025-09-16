from django.db import models
from django.conf import settings
from tables.models import Table
from menu.models import MenuItem


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="waiter_orders",
        limit_choices_to={'role': 'waiter'}
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="customer_orders",
        limit_choices_to={'role': 'customer'}
    )
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
