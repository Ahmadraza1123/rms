from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as drf_status


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('table', 'waiter', 'customer')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['pending', 'preparing', 'served', 'completed']:
            return Response({'error': 'Invalid status'}, status=drf_status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({'status': order.status})


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'menu_item')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
