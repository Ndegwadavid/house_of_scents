import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from django.contrib.sessions.models import Session

logger = logging.getLogger(__name__)

class CartView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET' and self.request.user.is_authenticated and self.request.user.role == 'admin':
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        if request.user.is_authenticated and request.user.role == 'admin':
            carts = Cart.objects.all()
            serializer = CartSerializer(carts, many=True)
            return Response(serializer.data)
        
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            logger.info(f"Created new session_key: {session_key}")

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            if created and session_key:
                guest_cart = Cart.objects.filter(session_key=session_key).first()
                if guest_cart:
                    for item in guest_cart.items.all():
                        CartItem.objects.create(cart=cart, product=item.product, quantity=item.quantity)
                    guest_cart.delete()
                    logger.info(f"Merged guest cart into user cart for user: {request.user.email}")
        else:
            cart, created = Cart.objects.get_or_create(session_key=session_key)
            if created:
                logger.info(f"Created new guest cart with session_key: {session_key}")

        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    def post(self, request):
        logger.info(f"Add to cart request with data: {request.data}")
        
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            logger.info(f"Created new session_key: {session_key}")

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        data = {
            'product_id': request.data.get('product_id'),
            'quantity': request.data.get('quantity', 1)
        }
        logger.info(f"Serializer input data: {data}")

        serializer = CartItemSerializer(data=data, context={'cart': cart})
        if serializer.is_valid():
            logger.info(f"Validated data - product: {serializer.validated_data['product'].name}, quantity: {serializer.validated_data['quantity']}")
            cart_item = serializer.save()
            logger.info(f"Cart item saved: {cart_item}")
            
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartView(APIView):
    def delete(self, request):
        logger.info(f"Remove from cart request with data: {request.data}")
        
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            logger.info(f"Authenticated user cart lookup for: {request.user.email}")
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
                logger.info(f"Created new session_key: {session_key}")
            cart = Cart.objects.filter(session_key=session_key).first()
            logger.info(f"Guest cart lookup with session_key: {session_key}")

        if not cart:
            logger.warning("Cart not found.")
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get('product_id')
        if not product_id:
            logger.error("Product ID not provided.")
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = cart.items.get(product_id=product_id)
            cart_item.delete()
            logger.info(f"Removed item: {product_id} from cart: {cart.id}")
        except CartItem.DoesNotExist:
            logger.warning(f"Item with product_id {product_id} not found in cart.")
            return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)