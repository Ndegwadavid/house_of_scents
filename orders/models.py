from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from users.models import User
from products.models import Product, Coupon
import uuid

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    DELIVERY_MODES = (
        ('pay_on_delivery', 'Pay on Delivery'),
        ('collect_at_shop', 'Collect at Shop'),
        ('pay_now', 'Pay Now'),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    order_id = models.CharField(max_length=20, unique=True, blank=True)  # e.g., HOS-20250427-0001
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    delivery_mode = models.CharField(max_length=20, choices=DELIVERY_MODES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Kenya')

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['guest_email']),
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        if not self.order_id:
            date_str = timezone.now().strftime('%Y%m%d')
            orders_today = Order.objects.filter(created_at__date=timezone.now().date()).count()
            sequence = f"{orders_today + 1:04d}"
            self.order_id = f"HOS-{date_str}-{sequence}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.email if self.user else self.guest_email or 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['order', 'product']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"