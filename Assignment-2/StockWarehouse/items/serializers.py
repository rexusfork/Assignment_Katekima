from rest_framework import serializers
from .models import Item


# DTO: Base Class
class ItemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["is_deleted"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]

# DTO: Update Item
class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude =  ["created_at", "is_deleted", "code"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]
