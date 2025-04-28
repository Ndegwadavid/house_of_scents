from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, RegisterSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered. Check email to verify.'}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(verification_token=token)
            if user.is_active:
                return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)
            user.is_active = True
            user.verification_token = None
            user.save()
            logger.info(f"Email verified for {user.email}")
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"Invalid verification token: {token}")
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)
            verification_token = str(uuid.uuid4())
            user.verification_token = verification_token
            user.save()
            verification_url = f"{settings.SITE_URL}/api/auth/verify-email/?token={verification_token}"
            try:
                send_mail(
                    subject='Verify Your House of Scents Account',
                    message=f'Hi {user.username},\n\nPlease verify your email by clicking: {verification_url}\n\nThank you!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
                logger.info(f"Resent verification email to {user.email}")
                return Response({'message': 'Verification email resent.'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Failed to resend verification email to {user.email}: {str(e)}")
                return Response({'message': 'Failed to resend verification email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except User.DoesNotExist:
            logger.warning(f"Resend verification requested for non-existent email: {email}")
            return Response({'message': 'Verification email resent.'}, status=status.HTTP_200_OK)  # Don't reveal email doesn't exist

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = str(uuid.uuid4())
                user.verification_token = token
                user.save()
                reset_url = f"{settings.SITE_URL}/api/auth/password-reset/confirm/?token={token}"
                try:
                    send_mail(
                        subject='Reset Your House of Scents Password',
                        message=f'Click to reset your password: {reset_url}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True
                    )
                    logger.info(f"Sent password reset email to {user.email}")
                except Exception as e:
                    logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
                return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                logger.warning(f"Password reset requested for non-existent email: {email}")
                return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(verification_token=token)
                user.set_password(new_password)
                user.verification_token = None
                user.save()
                tokens = OutstandingToken.objects.filter(user=user)
                for token in tokens:
                    BlacklistedToken.objects.get_or_create(token=token)
                logger.info(f"Password reset for {user.email}")
                return Response({'message': 'Password reset successfully. All previous sessions revoked.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                logger.error(f"Invalid password reset token: {token}")
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.email} logged out")
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout error for {request.user.email}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)