from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Category, Product, Coupon, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, CouponSerializer
from django.db.models import Q

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        query = self.request.query_params.get('q', None)
        category_id = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        in_stock = self.request.query_params.get('in_stock', None)
        is_new = self.request.query_params.get('is_new', None)
        sort = self.request.query_params.get('sort', None)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(scent__icontains=query)
            )
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(
                Q(discount_price__gte=min_price) |
                (Q(discount_price__isnull=True) & Q(price__gte=min_price))
            )
        if max_price:
            queryset = queryset.filter(
                Q(discount_price__lte=max_price) |
                (Q(discount_price__isnull=True) & Q(price__lte=max_price))
            )
        if in_stock == 'true':
            queryset = queryset.filter(stock__gt=0)
        if is_new == 'true':
            queryset = queryset.filter(is_new=True)
        if sort in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)

        return queryset
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class NewProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_new=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class FeaturedProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_featured=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        serializer.save(product=product)

class CouponValidateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            if not coupon.is_valid():
                return Response({'error': 'Coupon is expired or invalid.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = CouponSerializer(coupon)
            return Response(serializer.data)
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code.'}, status=status.HTTP_400_BAD_REQUEST)