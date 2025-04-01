from rest_framework import serializers
from .models import SellHeader, SellDetail


# DTO: Sell Header Base
class SellHeaderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        exclude = ["is_deleted"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]


# DTO: Sell Header Update
class SellHeaderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        exclude = ["is_deleted", "created_at", "code", "date"]
        read_only_fields = ["created_at", "updated_at", "is_deleted"]


# DTO: Sell Detail Base
class SellDetailBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        exclude = ["is_deleted"]
        extra_kwargs = {
            "header_code": {"read_only": True},
        }
