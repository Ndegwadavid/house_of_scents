from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'address', 'phone', 'role', 'receive_stock_alerts']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False
        )
        token = str(uuid.uuid4())
        user.verification_token = token
        user.save()
        verification_url = f"{settings.SITE_URL}/api/auth/verify-email/?token={token}"
        send_mail(
            subject='Verify Your House of Scents Account',
            message=f'Click to verify your email: {verification_url}',
            from_email='no-reply@houseofscents.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
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