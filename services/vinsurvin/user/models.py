from django.db import models
from django.contrib.auth.models import AbstractUser
from djongo import models as djongo_models
from django.utils import timezone
from django.db import transaction
from product.models import Product

class OrderLine(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        abstract = True

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=50)
    order_lines = djongo_models.ArrayField(
        model_container=OrderLine,
        default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    id = models.AutoField(primary_key=True, serialize=False)
    cart = djongo_models.JSONField(default=list, null=True, blank=True)
    orders = djongo_models.ArrayField(
        model_container=Order,
        default=list
    )
    last_order_id = models.PositiveIntegerField(default=0)

    @property
    def last_order_id(self):
        if self.orders:
            return max(order['order_id'] for order in self.orders)
        return 0

    def add_to_cart(self, product_id, quantity):
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product_id)
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
                
                if self.cart is None:
                    self.cart = []
                    
                cart_item = next((item for item in self.cart if item['product_id'] == product_id), None)
                if cart_item:
                    cart_item['quantity'] += quantity
                else:
                    self.cart.append({'product_id': product_id, 'quantity': quantity})
                self.save()
                return True
            return False
        
    def remove_from_cart(self, product_id, quantity=1):
        with transaction.atomic():
            if self.cart is None:
                return False
            item = next((item for item in self.cart if item['product_id'] == product_id), None)
            if item:
                product = Product.objects.get(pk=product_id)
                if item['quantity'] > quantity:
                    item['quantity'] -= quantity
                    product.release_stock(quantity)
                else:
                    quantity_to_release = item['quantity']
                    self.cart.remove(item)
                    product.release_stock(quantity_to_release)
                self.save()
                return True
            return False
    
    def delete_cart(self):
        self.cart = []
        self.save()
        
    def get_cart(self):
        return self.cart

    def create_order(self, status='pending'):
        new_order_number = self.last_order_id + 1
        order = {
            'order_id': new_order_number,
            'status': status,
            'order_lines': self.cart,
            'created_at': timezone.now()
        }
        if self.orders is None:
            self.orders = []
        self.orders.append(order)
        self.cart = []
        self.save()
        return order
    
    def update_order_status(self, order_number, new_status):
        for order in self.orders:
            if order.get('order_id') == order_number:
                order['status'] = new_status
                self.save()
                return True
        return False
    

    def get_orders(self):
        return self.orders
    
    def get_info(self):
        return {
            'username': self.username,
            'email': self.email,
            'createdAt': self.date_joined,
            'lastLogin': self.last_login
        }