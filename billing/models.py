from django.db import models
from orders.models import Order, OrderItem
from django.conf import settings
from decimal import Decimal


class Bill(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bill')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='bills',limit_choices_to={'role': 'cashier'}
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=20,
        choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')],
        default='cash'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_totals(self):

        self.subtotal = sum([item.menu_item.price * item.quantity for item in self.order.items.all()])

        self.tax = self.subtotal * Decimal("0.10")
        self.total_amount = self.subtotal - self.discount + self.tax
        return self.total_amount

