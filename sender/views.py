from django.http import JsonResponse
from sender.email_service import send_reservation_email, send_invoice_email, send_promotional_email

def test_reservation_email(request):
    send_reservation_email("customer@gmail.com", "Reservation Confirmed", "Your booking is confirmed.")
    return JsonResponse({"status": "success", "message": "Reservation email sent"})

def test_invoice_email(request):
    send_invoice_email("customer@gmail.com", "Invoice", "Your payment receipt is attached.")
    return JsonResponse({"status": "success", "message": "Invoice email sent"})

def test_promo_email(request):
    send_promotional_email("customer@gmail.com", "Special Offer!", "Get 20% OFF on your next booking.")
    return JsonResponse({"status": "success", "message": "Promotional email sent"})
