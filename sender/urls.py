from django.urls import path
from . import views

urlpatterns = [
    path("testreservation/", views.test_reservation_email, name="test_reservation_email"),
    path("testinvoice/", views.test_invoice_email, name="test_invoice_email"),
    path("testpromo/", views.test_promo_email, name="test_promo_email"),
]
