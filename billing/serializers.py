from rest_framework import serializers
from .models import Bill
from sender.email_service import send_invoice_email


class BillSerializer(serializers.ModelSerializer):
    cashier_name = serializers.CharField(source="cashier.username", read_only=True)

    class Meta:
        model = Bill
        fields = [
            "id",
            "order",
            "cashier",
            "cashier_name",
            "subtotal",
            "discount",
            "tax",
            "total_amount",
            "paid",
            "payment_method",
            "created_at",
        ]
        read_only_fields = ["subtotal", "tax", "total_amount", "created_at"]

    def create(self, validated_data):
        bill = Bill.objects.create(**validated_data)
        bill.calculate_totals()
        bill.save()


        order = bill.order
        if order.customer and order.customer.email:
            send_invoice_email(
                to_email=order.customer.email,
                subject="Your Payment Invoice",
                message=f"Hello {order.customer.username},\n\n"
                        f"Your bill for Order #{order.id} has been generated.\n"
                        f"Subtotal: Rs.{bill.subtotal}\n"
                        f"Discount: Rs.{bill.discount}\n"
                        f"Tax: Rs.{bill.tax}\n"
                        f"Total Amount: Rs.{bill.total_amount}\n"
                        f"Payment Method: {bill.payment_method}\n"
                        f"Paid: {'Yes' if bill.paid else 'No'}\n\n"
                        f"Thank you for your payment!"
            )

        return bill

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.calculate_totals()
        instance.save()


        order = instance.order
        if order.customer and order.customer.email:
            send_invoice_email(
                to_email=order.customer.email,
                subject="Your Updated Invoice",
                message=f"Hello {order.customer.username},\n\n"
                        f"Your bill for Order #{order.id} has been updated.\n"
                        f"Subtotal: Rs.{instance.subtotal}\n"
                        f"Discount: Rs.{instance.discount}\n"
                        f"Tax: Rs.{instance.tax}\n"
                        f"Total Amount: Rs.{instance.total_amount}\n"
                        f"Payment Method: {instance.payment_method}\n"
                        f"Paid: {'Yes' if instance.paid else 'No'}\n\n"
                        f"Thank you!"
            )

        return instance
