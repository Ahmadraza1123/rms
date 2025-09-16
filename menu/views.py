from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import IsAdminOrManager


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated ,IsAdminOrManager]


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated,IsAdminOrManager]
