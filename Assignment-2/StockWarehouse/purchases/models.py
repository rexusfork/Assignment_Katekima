from django.db import models
from items.models import Item


# Create your models here.
class PurchaseHeader(models.Model):
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    date = models.DateField()
    description = models.TextField(default="No description")

    # Mandatory
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class PurchaseDetail(models.Model):
    item_code = models.ForeignKey(Item, to_field="code", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.PositiveIntegerField()
    header_code = models.ForeignKey(
        PurchaseHeader,
        to_field="code",
        related_name="details",
        on_delete=models.CASCADE,
    )

    # Mandatory
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.header_code.code} - {self.item_code}"
