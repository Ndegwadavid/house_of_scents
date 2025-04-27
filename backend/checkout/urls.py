from django.urls import path
from .views import PaymentInitiateView, MpesaCallbackView, TransactionMessageUploadView

urlpatterns = [
    path('initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('upload-transaction/', TransactionMessageUploadView.as_view(), name='upload-transaction'),
]