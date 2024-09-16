from django.db import models
from djongo import models as djongo_models
from django.core.exceptions import ValidationError
from django.db import transaction


class Product(djongo_models.Model):
    numero = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=True)
    promo = models.FloatField(blank=True, null=True)
    description = models.TextField(null=True)
    image = models.CharField(max_length=255, null=True)
    stock = models.IntegerField(null=True)
    type = models.CharField(max_length=50, null=True)
    domain = models.CharField(max_length=50, blank=True, null=True)
    producer = models.CharField(max_length=50, blank=True, null=True)
    millesime = models.IntegerField(blank=True, null=True)
    grape_variety = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    appellation = models.CharField(max_length=50, blank=True, null=True)

    objects = djongo_models.DjongoManager()

    def __str__(self):
        return self.name or "Unnamed Product"
    
    def reserve_stock(self, quantity):
        with transaction.atomic():
            if self.stock >= quantity:
                self.stock -= quantity
                self.save()
                return True
            return False

    def release_stock(self, quantity):
        with transaction.atomic():
            self.stock += quantity
            self.save()


