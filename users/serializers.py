from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'address', 'phone', 'role', 'receive_stock_alerts']
        extra_kwargs = {
            'role': {'read_only': True},
            'receive_stock_alerts': {'required': False, 'default': False}
        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password', 'address', 'phone', 'receive_stock_alerts']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'receive_stock_alerts': {'required': False, 'default': False}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        verification_token = str(uuid.uuid4())
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            address=validated_data.get('address', ''),
            phone=validated_data.get('phone', ''),
            receive_stock_alerts=validated_data.get('receive_stock_alerts', False),
            verification_token=verification_token,
            is_active=False
        )
        verification_url = f"{settings.SITE_URL}/api/auth/verify-email/?token={verification_token}"
        try:
            send_mail(
                subject='Verify Your House of Scents Account',
                message=f'Hi {user.username},\n\nPlease verify your email by clicking: {verification_url}\n\nThank you!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )
            logger.info(f"Sent verification email to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)