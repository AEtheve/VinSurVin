from django.db import models
from django.contrib.auth.models import AbstractUser
from djongo import models as djongo_models

class User(AbstractUser):
    cart = djongo_models.JSONField(default=dict, null=True, blank=True)

    def add_to_cart(self, product_id, quantity):
        if self.cart is None:
            self.cart = []
        elif isinstance(self.cart, dict):
            self.cart = list(self.cart.values())
            
        item = next((item for item in self.cart if item['product_id'] == product_id), None)
        if item:
            item['quantity'] += quantity
        else:
            self.cart.append({'product_id': product_id, 'quantity': quantity})
        self.save()

    def remove_from_cart(self, product_id, quantity=1):
        if self.cart is None:
            return False
        item = next((item for item in self.cart if item['product_id'] == product_id), None)
        if item:
            if item['quantity'] > quantity:
                item['quantity'] -= quantity
            else:
                self.cart.remove(item)
            self.save()
            return True
        return False
        
    def get_cart(self):
        return self.cart