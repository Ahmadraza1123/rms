from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Bill
from .serializers import BillSerializer


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all().select_related("order", "cashier")
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cashier=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save(cashier=request.user)

        # custom response with full bill details
        return Response(
            {
                "order": bill.order.id,
                "subtotal": bill.subtotal,
                "discount": bill.discount,
                "tax": bill.tax,
                "total_amount": bill.total_amount,
                "payment_method": bill.payment_method,
                "paid": bill.paid,
                "created_at": bill.created_at,
                "cashier": bill.cashier.username if bill.cashier else None,
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        bill = self.get_object()
        bill.paid = True
        bill.payment_method = request.data.get("payment_method", "cash")
        bill.save()
        return Response(
            {
                "message": "Bill marked as paid",
                "order": bill.order.id,
                "total_amount": bill.total_amount,
                "payment_method": bill.payment_method,
                "paid": bill.paid,
            },
            status=status.HTTP_200_OK
        )
