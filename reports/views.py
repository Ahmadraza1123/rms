from django.db.models import Sum, Count, Avg, F, DecimalField, OuterRef, Subquery
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from menu.models import MenuItem
from tables.models import Table
from reviews.models import ServiceReview
from .permissions import IsAdminUser


class ReportsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]


    @action(detail=False, methods=["get"])
    def sales_report(self, request):
        today = timezone.now().date()


        daily = (
            OrderItem.objects.filter(order__created_at__date=today)
            .aggregate(total=Sum(F("menu_item__price") * F("quantity"),
                                 output_field=DecimalField()))["total"] or 0
        )
        weekly = (
            OrderItem.objects.filter(order__created_at__gte=today - timezone.timedelta(days=7))
            .aggregate(total=Sum(F("menu_item__price") * F("quantity"),
                                 output_field=DecimalField()))["total"] or 0
        )
        monthly = (
            OrderItem.objects.filter(order__created_at__gte=today.replace(day=1))
            .aggregate(total=Sum(F("menu_item__price") * F("quantity"),
                                 output_field=DecimalField()))["total"] or 0
        )

        return Response({
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly,
        })


    @action(detail=False, methods=["get"])
    def top_dishes(self, request):
        top_items = (
            MenuItem.objects.annotate(order_count=Count("orderitem"))
            .order_by("-order_count")[:5]
            .values("id", "description", "order_count")
        )
        return Response(top_items)

    @action(detail=False, methods=["get"])
    def customer_insights(self, request):

        order_totals = (
            Order.objects
            .filter(customer=OuterRef("pk"))
            .annotate(
                total=Sum(
                    F("items__menu_item__price") * F("items__quantity"),
                    output_field=DecimalField()
                )
            )
            .values("total")
        )


        insights = (
            Order.objects.values("customer__id", "customer__username")
            .annotate(
                total_orders=Count("id"),
                avg_spend=Subquery(order_totals[:1])
            )
            .order_by("-total_orders")[:5]
        )

        return Response(insights)

    @action(detail=False, methods=["get"])
    def table_utilization(self, request):
        utilization = (
            Table.objects.annotate(total_orders=Count("order"))
            .values("tables", "seats", "location", "total_orders")
            .order_by("-total_orders")
        )
        return Response(utilization)


    @action(detail=False, methods=["get"])
    def waiter_performance(self, request):
        performance = (
            ServiceReview.objects.values("waiter__id", "waiter__username")
            .annotate(
                orders_served=Count("order"),
                avg_rating=Avg("rating_waiter")
            )
            .order_by("-avg_rating")
        )
        return Response(performance)
