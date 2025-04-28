from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from dirtyfields import DirtyFieldsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['product'])]

    def __str__(self):
        return f"Image for {self.product.name}"

class Product(DirtyFieldsMixin, models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scent = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    photo = models.ImageField(upload_to='products/', null=True, blank=True)  # Keep for backward compatibility
    created_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['scent']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['discount_price']),
        ]

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.discount_price if self.discount_price is not None else self.price

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        indexes = [models.Index(fields=['product', 'user'])]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating} stars)"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g., "HOUSEOFSCENTS001"
    description = models.TextField(blank=True)
    discount_type = models.CharField(
        max_length=10,
        choices=[('percentage', 'Percentage')],
        default='percentage'
    )
    discount_value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]  # e.g., 80.00 for 80%
    )
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(null=True, blank=True)  # Null for unlimited
    uses = models.PositiveIntegerField(default=0)
    minimum_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]  # e.g., 1000.00 for KES 1000
    )

    class Meta:
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return self.code

    def is_valid(self, order_total=0):
        now = timezone.now()
        if not (
            self.active and
            self.valid_from <= now <= self.valid_until and
            (self.max_uses is None or self.uses < self.max_uses)
        ):
            return False
        if self.minimum_order_value and order_total < self.minimum_order_value:
            return False
        return True

    def apply_discount(self, amount):
        if not self.is_valid(amount):
            return amount
        discount = amount * (self.discount_value / 100)
        self.uses += 1
        self.save()
        return max(amount - discount, 0)

@receiver(post_save, sender=Product)
def send_stock_alert(sender, instance, **kwargs):
    # Disable alerts in development if DEBUG is True
    if settings.DEBUG:
        return

    # Only send alerts for significant restocks (stock from 0 to >=10)
    if (
        instance.stock >= 10 and
        instance.tracker.has_changed('stock') and
        instance.tracker.previous('stock') == 0
    ):
        cache_key = f"stock_alert_{instance.id}"
        if not cache.get(cache_key):
            users = User.objects.filter(receive_stock_alerts=True)
            messages = [
                (
                    f"Stock Alert: {instance.name} is Back in Stock!",
                    f"Our {instance.name} ({instance.scent} scent) is now available with {instance.stock} units.\nShop now: {settings.SITE_URL}/products/{instance.id}/",
                    'no-reply@houseofscents.com',
                    [user.email]
                )
                for user in users
            ]
            send_mass_mail(messages, fail_silently=True)
            # Set cache to prevent re-sending for 24 hours
            cache.set(cache_key, True, timeout=24 * 60 * 60)