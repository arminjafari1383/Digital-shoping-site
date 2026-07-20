import requests

from django.conf import settings

from .models import Payment


def request_payment(payment):

    data = {
        "merchant_id":
        settings.ZARINPAL_MERCHANT_ID,

        "amount":
        int(payment.amount),

        "description":
            "Online Shopping",
        
        "callback_url":
            "http://127.0.0.1:8000/api/payments/verify"
    
    }

    response = requests.post(
        settings.ZARINPAL_REQUEST_URL,
        json = data
    )

    result = response.json()

    if result.get("data"):
        authority = result["data"]["authority"]

        payment.authority = authority

        payment.save()

        return authority
    
    return None

