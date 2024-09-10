from django.db import models
from djongo import models as djongo_models
from django.core.exceptions import ValidationError

class Product(djongo_models.Model):
    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    promo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(null=True)
    image = models.URLField(null=True)
    stock = models.IntegerField(null=True)
    type = models.CharField(max_length=50, null=True)
    domain = models.CharField(max_length=50, blank=True, null=True)
    producer = models.CharField(max_length=50, blank=True, null=True)
    millesime = models.IntegerField(blank=True, null=True)

    objects = djongo_models.DjongoManager()

    def __str__(self):
        return self.name or "Unnamed Product"


