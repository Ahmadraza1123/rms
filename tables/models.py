from django.db import models
from accounts.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.timezone import now



def today_date():
    return timezone.now().date()


class Table(models.Model):
    tables = models.AutoField(primary_key=True)
    seats = models.IntegerField()
    location = models.CharField(
        max_length=50,
        choices=[('indoor', 'Indoor'), ('outdoor', 'Outdoor')]
    )
    status = models.CharField(max_length=20, default='available')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tables")



class Reservation(models.Model):
    table = models.ForeignKey("Table", on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=now)   # ✅ default = today
    time_slot = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status in ['pending', 'confirmed']:
            self.table.status = 'booked'
        elif self.status == 'cancelled':
            self.table.status = 'available'
        self.table.save()

    def delete(self, *args, **kwargs):
        self.table.status = 'available'
        self.table.save()
        super().delete(*args, **kwargs)
