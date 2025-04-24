from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity')
    readonly_fields = ('product', 'quantity')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'session_key', 'item_count', 'created_at', 'updated_at')
    search_fields = ('user__email', 'session_key')
    list_filter = ('created_at',)
    inlines = [CartItemInline]

    def user_email(self, obj):
        return obj.user.email if obj.user else 'Guest'
    user_email.short_description = 'User'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart_user', 'product_name', 'quantity')
    search_fields = ('cart__user__email', 'product__name')

    def cart_user(self, obj):
        return obj.cart.user.email if obj.cart.user else 'Guest'
    cart_user.short_description = 'User'

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'