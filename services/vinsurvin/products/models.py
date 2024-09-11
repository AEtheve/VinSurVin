from django.db import models
from djongo import models as djongo_models
from django.core.exceptions import ValidationError

class Product(djongo_models.Model):
    name = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True)
    image = models.CharField(max_length=255, null=True)    
    stock = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    millesime = models.IntegerField(blank=True, null=True)
    promo = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    producer = models.CharField(max_length=50, blank=True, null=True)
    grape_variety = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    appelation = models.CharField(max_length=50, blank=True, null=True)
    

    objects = djongo_models.DjongoManager()

    def __str__(self):
        return self.name or "Unnamed Product"


