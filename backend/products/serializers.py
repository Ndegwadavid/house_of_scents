from rest_framework import serializers
from .models import Category, Product, Review, Coupon, ProductImage
from users.models import User

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    masked_email = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'user_email', 'masked_email', 'rating', 'comment', 'created_at']
        read_only_fields = ['user_name', 'user_email', 'masked_email', 'created_at']

    def get_masked_email(self, obj):
        email = obj.user.email
        if not email:
            return ""
        local_part, domain = email.split('@')
        if len(local_part) <= 2:
            masked = local_part + '*****'
        else:
            masked = local_part[:2] + '*****'
        return f"{masked}@{domain}"

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'description', 'discount_type', 'discount_value', 'valid_from', 'valid_until', 'active', 'uses']
        read_only_fields = ['uses']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    photo = serializers.ImageField(required=False)
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'scent', 'price', 'discount_price', 'final_price',
            'stock', 'category', 'category_id', 'photo', 'created_at', 'is_new', 'is_featured',
            'reviews', 'images'
        ]

    def validate_photo(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:  # 2MB limit
                raise serializers.ValidationError("Image size must be under 2MB.")
            if not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise serializers.ValidationError("Only JPG or PNG images are allowed.")
        return value