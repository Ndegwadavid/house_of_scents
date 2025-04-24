from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer
from users.models import User  # Added import
from cart.models import Cart, CartItem

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', required=False, allow_null=True
    )

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'email', 'address', 'phone', 'order_number', 'tracking_number', 'status', 'total_amount', 'payment_status', 'created_at', 'items']

    def validate(self, data):
        items = data.get('items', [])
        if not items:
            raise serializers.ValidationError("Order must have at least one item.")
        total_amount = 0
        for item in items:
            product = item['product']
            quantity = item['quantity']
            if product.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}.")
            total_amount += product.price * quantity
        data['total_amount'] = total_amount
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            product.stock -= quantity
            product.save()
        # Clear cart for authenticated user
        if validated_data.get('user'):
            Cart.objects.filter(user=validated_data['user']).delete()
        return order