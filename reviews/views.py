from rest_framework import viewsets, permissions
from .models import DishReview, ServiceReview
from .serializers import DishReviewSerializer, ServiceReviewSerializer
from .permissions import IsCustomerOrReadOnly



class DishReviewViewSet(viewsets.ModelViewSet):
    queryset = DishReview.objects.select_related('menu_item', 'order', 'customer')
    serializer_class = DishReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_staff:
            qs = qs.filter(customer=user)

        menu_item = self.request.query_params.get('menu_item')
        order = self.request.query_params.get('order')
        if menu_item:
            qs = qs.filter(menu_item_id=menu_item)
        if order:
            qs = qs.filter(order_id=order)

        return qs



class ServiceReviewViewSet(viewsets.ModelViewSet):
    queryset = ServiceReview.objects.select_related('order', 'customer', 'waiter', 'table')
    serializer_class = ServiceReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_staff:
            qs = qs.filter(customer=user)


        waiter = self.request.query_params.get('waiter')
        order = self.request.query_params.get('order')
        if waiter:
            qs = qs.filter(waiter_id=waiter)
        if order:
            qs = qs.filter(order_id=order)

        return qs
