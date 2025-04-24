from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product
from products.serializers import ProductSerializer

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
        if product and quantity and product.stock < quantity:
            raise serializers.ValidationError(f"Not enough stock for {product.name}. Stock: {product.stock}, Requested: {quantity}")
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
            cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'items', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())