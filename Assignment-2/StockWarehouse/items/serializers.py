from rest_framework import serializers
from .models import Item


# DTO: Base Class
class ItemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["is_deleted", "updated_at", "created_at"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]


# DTO: Get List
class GetListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["is_deleted"]


# DTO: Update Item
class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "unit", "description", "stock", "balance"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]
