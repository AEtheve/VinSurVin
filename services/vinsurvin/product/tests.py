from django.test import TestCase
from django.db import transaction
from django.contrib.auth import get_user_model
from product.models import Product
from user.models import User
import threading

User = get_user_model()

class StockLockingTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", stock=10, price=100)
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

    def test_concurrent_stock_reservation(self):
        def add_to_cart_user1():
            with transaction.atomic():
                self.user1.add_to_cart(self.product.pk, 7)

        def add_to_cart_user2():
            with transaction.atomic():
                self.user2.add_to_cart(self.product.pk, 5)

        thread1 = threading.Thread(target=add_to_cart_user1)
        thread2 = threading.Thread(target=add_to_cart_user2)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(self.product.stock, 3)
        self.assertEqual(len(self.user1.cart), 1)
        self.assertEqual(len(self.user2.cart), 0)
        self.assertEqual(self.user1.cart[0]['quantity'], 7)

    def test_stock_overflow_prevention(self):
        result1 = self.user1.add_to_cart(self.product.pk, 8)
        result2 = self.user2.add_to_cart(self.product.pk, 5)

        self.assertTrue(result1)
        self.assertFalse(result2)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)