from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_email', 'status', 'total_price', 'created_at', 'estimated_delivery_date')
    list_filter = ('status', 'delivery_mode', 'created_at')
    search_fields = ('order_id', 'user__email', 'guest_email', 'address_line1', 'city')
    inlines = [OrderItemInline]
    list_editable = ('status', 'estimated_delivery_date')

    def customer_email(self, obj):
        return obj.user.email if obj.user else obj.guest_email or 'Guest'
    customer_email.short_description = 'Customer Email'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id_display', 'product_name', 'quantity', 'price')
    search_fields = ('order__order_id', 'product__name')

    def order_id_display(self, obj):
        return obj.order.order_id
    order_id_display.short_description = 'Order ID'

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'