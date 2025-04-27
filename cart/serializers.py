from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product, Coupon
from products.serializers import ProductSerializer
import logging

logger = logging.getLogger(__name__)

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    product_name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'product_name', 'quantity']

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        if product and quantity:
            if product.stock < quantity:
                logger.warning(f"Insufficient stock for {product.name}: Stock={product.stock}, Requested={quantity}")
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {quantity}"
                )
            if self.instance:
                current_quantity = self.instance.quantity
                additional_quantity = quantity - current_quantity
                if additional_quantity > 0 and product.stock < additional_quantity:
                    logger.warning(f"Cannot increase quantity for {product.name}: Stock={product.stock}, Additional={additional_quantity}")
                    raise serializers.ValidationError(
                        f"Not enough stock to increase quantity for {product.name}. Available: {product.stock}"
                    )
        return attrs

    def create(self, validated_data):
        cart = self.context['cart']
        product = validated_data['product']
        quantity = validated_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                logger.warning(f"Cannot add to cart {product.name}: Stock={product.stock}, Total={cart_item.quantity}")
                raise serializers.ValidationError(f"Not enough stock for {product.name}. Available: {product.stock}")
            cart_item.save()
        logger.info(f"Created/Updated cart item: {product.name}, Quantity={cart_item.quantity}")
        return cart_item

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    coupon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    coupon_discount = serializers.SerializerMethodField()
    delivery_mode = serializers.ChoiceField(choices=Cart.DELIVERY_MODES, required=False, allow_null=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'session_key', 'items', 'total_price', 'coupon', 'coupon_code',
            'coupon_discount', 'delivery_mode', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'session_key', 'items', 'total_price', 'coupon', 'coupon_discount', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        base_price = sum(item.product.final_price * item.quantity for item in obj.items.all())
        if obj.coupon and obj.coupon.is_valid(base_price):
            return obj.coupon.apply_discount(base_price)
        return base_price

    def get_coupon_discount(self, obj):
        base_price = sum(item.product.final_price * item.quantity for item in obj.items.all())
        if obj.coupon and obj.coupon.is_valid(base_price):
            return base_price - obj.coupon.apply_discount(base_price)
        return 0

    def validate_coupon_code(self, value):
        if value:
            try:
                coupon = Coupon.objects.get(code=value, active=True)
                base_price = sum(item.product.final_price * item.quantity for item in self.instance.items.all())
                if not coupon.is_valid(base_price):
                    logger.warning(f"Invalid coupon {value}: Base Price={base_price}, Min Order={coupon.minimum_order_value}")
                    raise serializers.ValidationError(
                        f"Coupon is invalid or order total is below minimum ({coupon.minimum_order_value or 'N/A'})."
                    )
            except Coupon.DoesNotExist:
                logger.warning(f"Coupon code not found: {value}")
                raise serializers.ValidationError("Invalid coupon code.")
        return value

    def validate(self, attrs):
        if 'delivery_mode' in attrs and attrs['delivery_mode'] not in dict(Cart.DELIVERY_MODES):
            logger.warning(f"Invalid delivery mode: {attrs['delivery_mode']}")
            raise serializers.ValidationError("Invalid delivery mode.")
        return attrs

    def update(self, instance, validated_data):
        coupon_code = validated_data.pop('coupon_code', None)
        delivery_mode = validated_data.pop('delivery_mode', None)
        instance = super().update(instance, validated_data)
        if coupon_code:
            instance.coupon = Coupon.objects.get(code=coupon_code)
            logger.info(f"Applied coupon {coupon_code} to cart {instance.id}")
        elif coupon_code == '':
            instance.coupon = None
            logger.info(f"Removed coupon from cart {instance.id}")
        if delivery_mode:
            instance.delivery_mode = delivery_mode
            logger.info(f"Set delivery mode {delivery_mode} for cart {instance.id}")
        instance.save()
        return instance