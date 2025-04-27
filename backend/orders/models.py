from django.db import models
from django.utils import timezone
from users.models import User
from products.models import Product, Coupon

class Order(models.Model):
    DELIVERY_MODES = (
        ('pay_on_delivery', 'Pay on Delivery'),
        ('collect_at_shop', 'Collect at Shop'),
        ('pay_now', 'Pay Now'),
    )
    ORDER_STATUSES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    delivery_mode = models.CharField(max_length=20, choices=DELIVERY_MODES)
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    estimated_delivery_date = models.DateTimeField()  # Changed to DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['user', 'created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.order_id:
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_id__startswith=f'HOS-{date_str}').order_by('-order_id').first()
            if last_order:
                last_number = int(last_order.order_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_id = f'HOS-{date_str}-{new_number:04d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"