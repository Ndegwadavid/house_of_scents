from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Order
from .serializers import OrderSerializer
from django.db.models import Q
from cart.models import Cart

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(Q(user=user) | Q(email=user.email))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.data.get('items'):
            cart = Cart.objects.filter(user=request.user).first()
            if not cart or not cart.items.exists():
                return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
            items = [{'product_id': item.product.id, 'quantity': item.quantity} for item in cart.items.all()]
            request.data['items'] = items
            request.data['email'] = request.user.email
            request.data['user_id'] = request.user.id
        return super().post(request, *args, **kwargs)

class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]