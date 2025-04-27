from django.db import models
from orders.models import Order
from users.models import User
from django.core.validators import RegexValidator

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('mpesa_stk', 'M-Pesa STK Push'),
        ('till_number', 'Till Number'),
    )
    PAYMENT_STATUSES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    guest_email = models.EmailField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default='pending')
    transaction_id = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(
        max_length=12,
        validators=[RegexValidator(regex=r'^\+254\d{9}$', message='Phone number must be in the format +254XXXXXXXXX')],
        blank=True,
        default=''  # Added default for clarity
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Payment {self.transaction_id or 'Pending'} for Order {self.order.order_id}"

class MpesaTransactionMessage(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transaction_messages')
    message_text = models.TextField()
    transaction_code = models.CharField(max_length=20, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction Message for Payment {self.payment.id}"