from django.contrib import admin
from .models import Payment, MpesaTransactionMessage

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id_display', 'payment_method', 'payment_status', 'amount', 'transaction_id', 'created_at')
    list_filter = ('payment_method', 'payment_status')
    search_fields = ('order__order_id', 'transaction_id', 'user__email', 'guest_email')

    def order_id_display(self, obj):
        return obj.order.order_id
    order_id_display.short_description = 'Order ID'

@admin.register(MpesaTransactionMessage)
class MpesaTransactionMessageAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'transaction_code', 'uploaded_at')
    search_fields = ('transaction_code', 'message_text')