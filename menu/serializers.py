from rest_framework import serializers
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source="category",write_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "category_id", "category", "category_items", "description", "price", "is_available", "created_at"]
