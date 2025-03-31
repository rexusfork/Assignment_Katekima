from django.db import models
from items.models import Item


# Create your models here.
class SellHeader(models.Model):
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class SellDetail(models.Model):
    header_code = models.ForeignKey(
        SellHeader, to_field="code", related_name="details", on_delete=models.CASCADE
    )
    item_code = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.header.code} - {self.item_code}"
