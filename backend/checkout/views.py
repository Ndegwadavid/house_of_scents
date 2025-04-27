from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Payment, MpesaTransactionMessage
from .serializers import PaymentSerializer, MpesaTransactionMessageSerializer
from orders.models import Order
from django.conf import settings
from django.core.mail import send_mail
import logging
import uuid
import threading
import time

logger = logging.getLogger(__name__)

# Commented out Daraja integration for future use
"""
from daraja.mpesa import MpesaClient
mpesa_client = MpesaClient(
    consumer_key=settings.DARAJA_CONSUMER_KEY,
    consumer_secret=settings.DARAJA_CONSUMER_SECRET,
    environment='sandbox'
)
"""

class PaymentInitiateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                payment = serializer.save()  # Use serializer to create payment
                order = serializer.validated_data['order']
                payment_method = serializer.validated_data['payment_method']
                phone_number = serializer.validated_data.get('phone_number', '')

                if payment_method == 'mpesa_stk':
                    # Simulate STK Push
                    try:
                        checkout_request_id = f"TEST-{uuid.uuid4().hex[:10]}"
                        payment.transaction_id = checkout_request_id
                        payment.save()
                        logger.info(f"Simulated STK Push for Order {order.order_id}, Transaction ID: {payment.transaction_id}")

                        def simulate_callback():
                            time.sleep(5)
                            payment.payment_status = 'completed'
                            payment.order.status = 'confirmed'
                            payment.order.save()
                            payment.save()
                            logger.info(f"Simulated callback completed for Transaction {checkout_request_id}")

                        threading.Thread(target=simulate_callback).start()

                        """
                        # Real Daraja STK Push
                        response = mpesa_client.stk_push(
                            phone_number=phone_number,
                            amount=int(order.total_price),
                            account_reference=order.order_id,
                            transaction_desc=f"Payment for Order {order.order_id}",
                            callback_url=settings.DARAJA_CALLBACK_URL
                        )
                        payment.transaction_id = response.get('CheckoutRequestID')
                        payment.save()
                        logger.info(f"Initiated STK Push for Order {order.order_id}, Transaction ID: {payment.transaction_id}")
                        """
                    except Exception as e:
                        logger.error(f"Simulated STK Push failed for Order {order.order_id}: {str(e)}")
                        payment.payment_status = 'failed'
                        payment.save()
                        return Response({'error': 'Failed to initiate M-Pesa payment.'}, status=status.HTTP_400_BAD_REQUEST)

                # Send email confirmation
                receipt_lines = [
                    f"House of Scents - Order Confirmation",
                    f"Order ID: {order.order_id}",
                    f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                    f"Customer: {order.user.email if order.user else order.guest_email or 'Guest'}",
                    f"Payment Method: {payment.get_payment_method_display()}",
                    f"Payment Status: {payment.get_payment_status_display()}",
                    f"Delivery Mode: {order.get_delivery_mode_display()}",
                    f"Address: {order.address_line1}, {order.address_line2}, {order.city}, {order.postal_code}, {order.country}",
                    f"\nItems:",
                ]
                for item in order.items.all():
                    receipt_lines.append(f"  {item.quantity} x {item.product.name} @ KES {item.price} = KES {item.quantity * item.price}")
                receipt_lines.extend([
                    f"\nSubtotal: KES {sum(item.quantity * item.price for item in order.items.all())}",
                    f"Coupon Discount: KES {sum(item.quantity * item.price for item in order.items.all()) - order.total_price}",
                    f"Total: KES {order.total_price}",
                    f"Estimated Delivery: {order.estimated_delivery_date.strftime('%Y-%m-%d %H:%M:%S')}",
                ])
                if payment_method == 'till_number':
                    receipt_lines.extend([
                        f"\nTill Number Payment Instructions:",
                        f"Please send KES {order.total_price} to Till Number: {settings.TILL_NUMBER}",
                        f"After payment, upload your M-Pesa transaction message at: http://localhost:8000/api/checkout/upload-transaction/",
                    ])
                receipt_lines.append(f"\nThank you for shopping with House of Scents!")

                try:
                    recipient = order.user.email if order.user else order.guest_email
                    send_mail(
                        subject=f'Order Confirmation - House of Scents #{order.order_id}',
                        message="\n".join(receipt_lines),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient],
                        fail_silently=True
                    )
                    logger.info(f"Sent confirmation email to {recipient} for Order {order.order_id}")
                except Exception as e:
                    logger.error(f"Failed to send confirmation email to {recipient}: {str(e)}")

                return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Payment creation failed: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = data.get('CheckoutRequestID')
        result_code = data.get('ResultCode')
        result_desc = data.get('ResultDesc')

        try:
            payment = Payment.objects.get(transaction_id=checkout_request_id)
            if result_code == 0:
                payment.payment_status = 'completed'
                payment.order.status = 'confirmed'
                payment.order.save()
                logger.info(f"Payment {checkout_request_id} completed for Order {payment.order.order_id}")
            else:
                payment.payment_status = 'failed'
                logger.warning(f"Payment {checkout_request_id} failed: {result_desc}")
            payment.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            logger.error(f"Callback received for unknown CheckoutRequestID: {checkout_request_id}")
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

class TransactionMessageUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(
                order_id=order_id,
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None
            )
            payment = Payment.objects.get(order=order, payment_method='till_number')
        except (Order.DoesNotExist, Payment.DoesNotExist):
            logger.warning(f"Order {order_id} or payment not found for user {request.user.email if request.user.is_authenticated else 'Guest'}")
            return Response({'error': 'Order or payment not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MpesaTransactionMessageSerializer(
            data=request.data,
            context={'payment': payment}
        )
        if serializer.is_valid():
            transaction_message = serializer.save(payment=payment)
            logger.info(f"Transaction message uploaded for Order {order_id}, Transaction Code: {serializer.validated_data.get('transaction_code', '')}")

            try:
                send_mail(
                    subject=f'New M-Pesa Transaction Message for Order {order_id}',
                    message=f"User uploaded transaction message for Order {order_id}.\n\nMessage: {serializer.validated_data['message_text']}\nTransaction Code: {serializer.validated_data.get('transaction_code', '')}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['admin@houseofscents.com'],
                    fail_silently=True
                )
                logger.info(f"Sent transaction message notification for Order {order_id}")
            except Exception as e:
                logger.error(f"Failed to send transaction message notification: {str(e)}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)