from rest_framework import serializers
from .models import DishReview, ServiceReview



class DishReviewSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DishReview
        fields = ['id', 'customer', 'menu_item', 'order', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        request_user = self.context['request'].user
        order = attrs.get('order')
        menu_item = attrs.get('menu_item')

        print("[LOGIN]", order.customer.id, request_user.id)
        if order.customer != request_user:
            raise serializers.ValidationError("You can only review your own orders.")


        if order.status != 'completed':
            raise serializers.ValidationError(" You can only review completed orders.")


        if not order.items.filter(menu_item=menu_item).exists():
            raise serializers.ValidationError(" This dish was not part of your order.")

        return attrs



class ServiceReviewSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ServiceReview
        fields = ['id', 'customer', 'order', 'waiter', 'table',
                  'rating_waiter', 'rating_table', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        request_user = self.context['request'].user
        order = attrs.get('order')


        if order.customer != request_user:
            raise serializers.ValidationError("you can only review your own orders.")


        if order.status != 'completed':
            raise serializers.ValidationError(" You can only review completed orders.")


        if not attrs.get('rating_waiter') and not attrs.get('rating_table'):
            raise serializers.ValidationError("At least one rating (waiter/table) is required.")

        return attrs
