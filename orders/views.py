from rest_framework import viewsets, status as drf_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('table', 'waiter', 'customer').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        allowed_status = ['pending', 'preparing', 'served', 'completed']

        if new_status not in allowed_status:
            return Response(
                {"error": f"Invalid status. Allowed: {allowed_status}"},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        order.status = new_status
        order.save()
        return Response(
            {"message": "Order status updated successfully", "status": order.status},
            status=drf_status.HTTP_200_OK
        )


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'menu_item')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
