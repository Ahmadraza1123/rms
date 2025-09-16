from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source="menu_item",
        write_only=True
    )
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    category_name = serializers.CharField(source='menu_item.category.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item_id', 'menu_item_name', 'category_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(source='items', many=True, read_only=True)
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'table', 'waiter', 'customer', 'status', 'created_at', 'items', 'order_items']
        read_only_fields = ['waiter', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = self.context.get('request')

        # waiter assign karna
        if request and request.user.role == 'waiter':
            validated_data['waiter'] = request.user

        validated_data['status'] = 'pending'
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
