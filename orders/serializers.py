from rest_framework import serializers
from tables.models import Reservation
from .models import Order, OrderItem
from menu.models import MenuItem
from sender.email_service import send_invoice_email


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source="menu_item",
        write_only=True
    )
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    category_name = serializers.CharField(source='menu_item.category.name', read_only=True)
    item_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'menu_item_id',
            'menu_item_name',
            'category_name',
            'quantity',
            'item_total',
        ]

    def get_item_total(self, obj):
        return obj.item_total()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(source='items', many=True, read_only=True)
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'table',
            'waiter',
            'customer',
            'status',
            'created_at',
            'items',
            'order_items',
            'total_amount',
        ]
        read_only_fields = ['waiter', 'created_at', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = self.context.get('request')


        if request and hasattr(request.user, "role") and request.user.role == 'waiter':
            validated_data['waiter'] = request.user

        validated_data['status'] = 'pending'
        table_obj = validated_data.get("table")


        reservation = Reservation.objects.filter(table=table_obj).first()
        if reservation:
            validated_data['customer'] = reservation.customer
        else:

            validated_data['customer'] = request.user


        order = Order.objects.create(**validated_data)


        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)


        if order.customer and order.customer.email:
            send_invoice_email(
                to_email=order.customer.email,
                subject="Order Confirmation",
                message=f"Dear {order.customer.username},\n\nYour order #{order.id} "
                        f"has been placed successfully.\nTotal: Rs.{order.total_amount()}.\n\nThank you!"
            )

        return order

    def get_total_amount(self, obj):
        return obj.total_amount()
