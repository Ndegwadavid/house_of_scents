from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Order
from .serializers import OrderSerializer
import logging

logger = logging.getLogger(__name__)

class OrderCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            logger.info(f"Order {order.order_id} created by {order.user.email if order.user else order.guest_email or 'Guest'}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Order creation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(APIView):
    def get_permissions(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request):
        if not request.user.is_authenticated:
            logger.info("Unauthenticated user attempted to access order list; redirecting to login")
            return Response(
                {'error': 'Authentication required.', 'redirect': '/api/auth/login/'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if request.user.role == 'admin':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        if not request.user.is_authenticated:
            logger.info(f"Unauthenticated user attempted to access order {order_id}; redirecting to login")
            return Response(
                {'error': 'Authentication required.', 'redirect': '/api/auth/login/'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found for user {request.user.email}")
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

class OrderReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        if not request.user.is_authenticated:
            logger.info(f"Unauthenticated user attempted to access receipt for order {order_id}; redirecting to login")
            return Response(
                {'error': 'Authentication required.', 'redirect': '/api/auth/login/'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
            receipt_lines = [
                f"House of Scents - Order Receipt",
                f"Order ID: {order.order_id}",
                f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Customer: {order.user.email if order.user else order.guest_email or 'Guest'}",
                f"Delivery Mode: {order.get_delivery_mode_display()}",
                f"Address: {order.address_line1}, {order.address_line2}, {order.city}, {order.postal_code}, {order.country}",
                f"\nItems:",
            ]
            total_price = sum(item.quantity * item.price for item in order.items.all())
            for item in order.items.all():
                receipt_lines.append(f"  {item.quantity} x {item.product.name} @ KES {item.price} = KES {item.quantity * item.price}")
            receipt_lines.extend([
                f"\nSubtotal: KES {total_price}",
                f"Coupon Discount: KES {total_price - order.total_price if order.coupon else 0}",
                f"Total: KES {order.total_price}",
                f"Estimated Delivery: {order.estimated_delivery_date}",
                f"\nThank you for shopping with House of Scents!"
            ])
            receipt_text = "\n".join(receipt_lines)
            return Response({'receipt': receipt_text})
        except Order.DoesNotExist:
            logger.warning(f"Order {order_id} not found for user {request.user.email}")
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)