from django.db import models
from django.contrib.auth.models import User
from core.models import Product
from coupons.models import Coupon
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    # Shipping info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='US')

    # Coupon
    coupon = models.ForeignKey(
        Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(default=0, help_text="Percentage discount applied")

    # Status & payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=250, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order #{self.id} — {self.get_status_display()}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def subtotal(self):
        return sum(item.get_total_price() for item in self.items.all())

    @property
    def discount_amount(self):
        if self.discount:
            return (Decimal(self.discount) / Decimal(100)) * self.subtotal
        return Decimal(0)

    @property
    def total(self):
        return self.subtotal - self.discount_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    def get_total_price(self):
        return self.price * self.quantity
