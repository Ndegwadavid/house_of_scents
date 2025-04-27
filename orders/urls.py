from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView, OrderReceiptView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order-create'),
    path('list/', OrderListView.as_view(), name='order-list'),
    path('<str:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('receipt/<str:order_id>/', OrderReceiptView.as_view(), name='order-receipt'),
]