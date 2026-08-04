from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Payment
from .services import request_payment
from django.conf import settings
from notifications.services import create_notification
from notifications.models import Notification

from order.models import Order



class StartPaymentView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, payment_id):

        payment = Payment.objects.get(
            id=payment_id,
            order__user=request.user
        )

        authority = request_payment(payment)

        if authority:
            
            url = (
                settings.ZARINPAL_START_URL
                + 
                authority
            )

            return Response({
                "payment_url":url
            })
        
        return Response(
            {
                "error":"Payment request failed"
            },
            status = 400

        )

class VerifyPaymentView(APIView):

    def get(self,request):

        authority = request.GET.get(
            "Authority"
        )

        status = request.GET.get(
            "Status"
        )

        if status != "OK":
            return Response({

                "message":
                "Payment cancelled"
            })
        
        payment = get_object_or_404(
            Payment,
            authority=authority
        )

        if payment.status == Payment.Status.SUCCESS:
            return Response({
                "message":"Payment already verified"
            })
        payment.status = (
            Payment.Status.SUCCESS
        )

        payment.save()

        create_notification(
            user = payment.order.user,
            title="Payment Successful",
            message="Your payment was completed successfully.",
            notification_type=Notification.Type.PAYMENT,
        )

        order = payment.order
        
        order.status = Order.Status.PAID

        order.save()

        return Response({

            "message":
            "Payment successful"
        })
    