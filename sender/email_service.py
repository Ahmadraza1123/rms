from django.core.mail import send_mail
from django.conf import settings


def send_email(to_email, subject, message):

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )


def send_reservation_email(to_email, subject, message):

    send_email(to_email, subject, message)


def send_invoice_email(to_email, subject, message):

    send_email(to_email, subject, message)


def send_promotional_email(to_email, subject, message):


    send_email(to_email, subject, message)
