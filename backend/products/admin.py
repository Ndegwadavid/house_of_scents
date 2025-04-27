from django.contrib import admin
from .models import Category, Product, Review, Coupon

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'scent', 'price', 'discount_price', 'stock', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description', 'scent')
    ordering = ('name',)
    list_editable = ('price', 'discount_price', 'stock', 'is_featured')
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')
    ordering = ('-created_at',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_until', 'active', 'uses')
    list_filter = ('discount_type', 'active')
    search_fields = ('code', 'description')
    ordering = ('-valid_from',)
    fields = ('code', 'description', 'discount_type', 'discount_value', 'valid_from', 'valid_until', 'active', 'max_uses', 'uses')