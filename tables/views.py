from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Table, Reservation
from .serializers import TableSerializer, ReservationSerializer
from .permissions import IsAdminOrManager, IsCustomer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':

            return Reservation.objects.filter(customer=user)

        return Reservation.objects.all()

    def perform_create(self, serializer):
        user = self.request.user


        if user.role == 'customer' and Reservation.objects.filter(customer=user).exists():
            raise serializers.ValidationError("Aap already ek table book kar chuke hain.")


        serializer.save(customer=user)
