from rest_framework import serializers
from .models import PurchaseHeader, PurchaseDetail


# DTO: Purchase Header Base
class PurchaseHeaderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHeader
        exclude = ["is_deleted"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]


# DTO: Purchase Header Update
class PurchaseHeaderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHeader
        fields = ["description", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]


# DTO: Purchase Detail Base
class PurchaseDetailBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        exclude = ["is_deleted"]
        extra_kwargs = {"header_code": {"read_only": True}}
