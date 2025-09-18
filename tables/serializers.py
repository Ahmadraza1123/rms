from rest_framework import serializers
from .models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['tables', 'seats', 'location', 'status']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.id')

    class Meta:
        model = Reservation
        fields = ['id', 'table', 'customer', 'date', 'time_slot', 'status']

    def validate(self, data):
        table = data.get("table")
        date = data.get("date")
        time_slot = data.get("time_slot")

        if Reservation.objects.filter(table=table, date=date, time_slot=time_slot).exists():
            raise serializers.ValidationError(
                "This table is already booked for the selected date and time slot."
            )
        return data
