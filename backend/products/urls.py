from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ProductListCreateView, ProductDetailView,
    NewProductsView, FeaturedProductsView,
    ReviewCreateView, CouponValidateView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('new/', NewProductsView.as_view(), name='new-products'),
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('coupons/validate/', CouponValidateView.as_view(), name='coupon-validate'),
]