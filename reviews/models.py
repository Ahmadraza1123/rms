from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL


class DishReview(models.Model):
    customer = models.ForeignKey(User, related_name='dish_reviews', on_delete=models.CASCADE)
    menu_item = models.ForeignKey('menu.MenuItem', related_name='reviews', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', related_name='dish_reviews', on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('order', 'menu_item')
        ordering = ['-created_at']




class ServiceReview(models.Model):
    customer = models.ForeignKey(User, related_name='service_reviews', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', related_name='service_reviews', on_delete=models.CASCADE)

    waiter = models.ForeignKey(User, related_name='received_service_reviews',on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey('tables.Table', related_name='service_reviews',on_delete=models.SET_NULL, null=True, blank=True)

    rating_waiter = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True, blank=True)
    rating_table = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

