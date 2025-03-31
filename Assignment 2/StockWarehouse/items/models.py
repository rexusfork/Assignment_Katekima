from django.db import models

# Create your models here.
class Item(models.Model):
    code = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Mandatory
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
