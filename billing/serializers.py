from rest_framework import serializers
from .models import Bill


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
        return bill

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)


        instance.calculate_totals()
        instance.save()
        return instance
