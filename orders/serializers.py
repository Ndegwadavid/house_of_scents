from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product, Coupon
from products.serializers import ProductSerializer
from cart.models import Cart
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()
    coupon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    guest_email = serializers.EmailField(write_only=True, required=False)
    address_line1 = serializers.CharField(write_only=True)
    address_line2 = serializers.CharField(write_only=True, required=False, allow_blank=True)
    city = serializers.CharField(write_only=True)
    postal_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    country = serializers.CharField(write_only=True, default='Kenya')
    delivery_mode = serializers.ChoiceField(choices=Order.DELIVERY_MODES, write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'user', 'session_key', 'guest_email', 'coupon', 'coupon_code', 'delivery_mode',
            'status', 'total_price', 'items', 'address', 'estimated_delivery_date', 'created_at', 'updated_at',
            'address_line1', 'address_line2', 'city', 'postal_code', 'country'
        ]
        read_only_fields = ['id', 'order_id', 'user', 'session_key', 'coupon', 'status', 'total_price', 'items', 'created_at', 'updated_at']

    def get_address(self, obj):
        return {
            'line1': obj.address_line1,
            'line2': obj.address_line2,
            'city': obj.city,
            'postal_code': obj.postal_code,
            'country': obj.country
        }

    def validate(self, attrs):
        request = self.context['request']
        delivery_mode = attrs.get('delivery_mode')
        if delivery_mode not in dict(Order.DELIVERY_MODES):
            logger.warning(f"Invalid delivery mode: {delivery_mode}")
            raise serializers.ValidationError("Invalid delivery mode.")
        
        if not request.user.is_authenticated and not attrs.get('guest_email'):
            logger.warning("Guest checkout attempted without email")
            raise serializers.ValidationError("Guest email is required for non-authenticated users.")
        
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key
        coupon_code = validated_data.pop('coupon_code', None)
        guest_email = validated_data.pop('guest_email', None)
        delivery_mode = validated_data.pop('delivery_mode')
        
        cart = Cart.objects.filter(user=user, session_key=session_key).first()
        if not cart or not cart.items.exists():
            logger.warning(f"Checkout attempted with empty cart: user={user}, session_key={session_key}")
            raise serializers.ValidationError("Cart is empty.")

        # Set delivery_mode on cart if not already set
        if not cart.delivery_mode:
            cart.delivery_mode = delivery_mode
            cart.save()
            logger.info(f"Set delivery_mode {delivery_mode} on cart {cart.id}")

        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                base_price = sum(item.product.final_price * item.quantity for item in cart.items.all())
                if not coupon.is_valid(base_price):
                    logger.warning(f"Invalid coupon {coupon_code} for order total {base_price}")
                    raise serializers.ValidationError(
                        f"Coupon is invalid or order total is below minimum ({coupon.minimum_order_value or 'N/A'})."
                    )
            except Coupon.DoesNotExist:
                logger.warning(f"Coupon code not found: {coupon_code}")
                raise serializers.ValidationError("Invalid coupon code.")

        total_price = sum(item.product.final_price * item.quantity for item in cart.items.all())
        discounted_price = total_price
        if coupon:
            discounted_price = coupon.apply_discount(total_price)

        order = Order.objects.create(
            user=user,
            session_key=session_key,
            guest_email=guest_email,
            coupon=coupon,
            delivery_mode=cart.delivery_mode,
            total_price=discounted_price,
            address_line1=validated_data['address_line1'],
            address_line2=validated_data.get('address_line2', ''),
            city=validated_data['city'],
            postal_code=validated_data.get('postal_code', ''),
            country=validated_data.get('country', 'Kenya'),
            estimated_delivery_date=timezone.now().date() + timezone.timedelta(days=7)
        )

        for item in cart.items.all():
            if item.quantity > item.product.stock:
                logger.warning(f"Insufficient stock for {item.product.name}: Stock={item.product.stock}, Requested={item.quantity}")
                raise serializers.ValidationError(f"Not enough stock for {item.product.name}. Available: {item.product.stock}")
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.final_price
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()
        cart.coupon = None
        cart.delivery_mode = None
        cart.save()

        receipt_lines = [
            f"House of Scents - Order Receipt",
            f"Order ID: {order.order_id}",
            f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Customer: {order.user.email if order.user else order.guest_email or 'Guest'}",
            f"Delivery Mode: {order.get_delivery_mode_display()}",
            f"Address: {order.address_line1}, {order.address_line2}, {order.city}, {order.postal_code}, {order.country}",
            f"\nItems:",
        ]
        for item in order.items.all():
            receipt_lines.append(f"  {item.quantity} x {item.product.name} @ KES {item.price} = KES {item.quantity * item.price}")
        receipt_lines.extend([
            f"\nSubtotal: KES {total_price}",
            f"Coupon Discount: KES {total_price - discounted_price if coupon else 0}",
            f"Total: KES {order.total_price}",
            f"Estimated Delivery: {order.estimated_delivery_date}",
            f"\nThank you for shopping with House of Scents!"
        ])
        receipt_text = "\n".join(receipt_lines)

        try:
            recipient = user.email if user else guest_email
            send_mail(
                subject=f'Order Confirmation - House of Scents #{order.order_id}',
                message=receipt_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=True
            )
            logger.info(f"Sent order confirmation and receipt to {recipient} for order {order.order_id}")
        except Exception as e:
            logger.error(f"Failed to send order confirmation to {recipient}: {str(e)}")

        return order