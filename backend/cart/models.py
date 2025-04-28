from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product, Coupon
from django.utils import timezone

class Cart(models.Model):
    DELIVERY_MODES = (
        ('pay_on_delivery', 'Pay on Delivery'),
        ('collect_at_shop', 'Collect at Shop'),
        ('pay_now', 'Pay Now'),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    delivery_mode = models.CharField(max_length=20, choices=DELIVERY_MODES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f"Cart for {self.user.email if self.user else 'Guest'} ({self.session_key})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        indexes = [
            models.Index(fields=['cart', 'product']),
        ]
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"