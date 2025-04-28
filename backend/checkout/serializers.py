from rest_framework import serializers
from .models import Payment, MpesaTransactionMessage
from orders.models import Order
import logging
from django.core.validators import RegexValidator

logger = logging.getLogger(__name__)

class MpesaTransactionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransactionMessage
        fields = ['id', 'payment', 'message_text', 'transaction_code', 'uploaded_at']
        read_only_fields = ['id', 'payment', 'uploaded_at']

    def validate(self, attrs):
        # Ensure payment exists and is for till_number
        payment = self.context.get('payment')
        if not payment:
            raise serializers.ValidationError("Payment must be provided")
        if payment.payment_method != 'till_number':
            raise serializers.ValidationError("Transaction messages are only allowed for Till Number payments")
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(write_only=True)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHODS)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    guest_email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_id', 'user', 'guest_email', 'payment_method', 'payment_status',
            'transaction_id', 'amount', 'phone_number', 'transaction_messages', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'order', 'user', 'payment_status', 'transaction_id', 'amount', 'transaction_messages',
            'created_at', 'updated_at'
        ]

    def validate(self, attrs):
        request = self.context['request']
        order_id = attrs.get('order_id')
        payment_method = attrs.get('payment_method')
        phone_number = attrs.get('phone_number', '')
        guest_email = attrs.get('guest_email')

        # Validate order
        try:
            order = Order.objects.get(
                order_id=order_id,
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None
            )
            attrs['order'] = order
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found for user {request.user or 'guest'}")
            raise serializers.ValidationError("Order not found or does not belong to user")

        # Check for existing payment (OneToOneField)
        if Payment.objects.filter(order=order).exists():
            logger.warning(f"Payment already exists for Order {order_id}")
            raise serializers.ValidationError("A payment already exists for this order")

        # Validate phone_number format if provided
        if phone_number:
            validator = RegexValidator(regex=r'^\+254\d{9}$', message='Phone number must be in the format +254XXXXXXXXX')
            validator(phone_number)

        # Require phone_number for mpesa_stk
        if payment_method == 'mpesa_stk' and not phone_number:
            raise serializers.ValidationError("Phone number is required for M-Pesa STK Push")

        # Require guest_email for non-authenticated users
        if not request.user.is_authenticated and not guest_email:
            raise serializers.ValidationError("Guest email is required for non-authenticated users")

        return attrs

    def create(self, validated_data):
        order = validated_data.pop('order')
        payment_method = validated_data.pop('payment_method')
        phone_number = validated_data.get('phone_number', '')  # Default to empty string
        guest_email = validated_data.get('guest_email')
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None

        payment = Payment.objects.create(
            order=order,
            user=user,
            guest_email=guest_email,
            payment_method=payment_method,
            payment_status='pending',
            amount=order.total_price,
            phone_number=phone_number
        )
        logger.info(f"Payment initiated for order {order.order_id}: {payment_method}")
        return payment