from django.urls import path

from .views import (
    StartPaymentView,
    VerifyPaymentView
)

urlpatterns = [
    path(
        "start/<uuid:payment_id>/",
        StartPaymentView.as_view()
    ),

    path(
        "verify/",
        VerifyPaymentView.as_view()
    ),
    
]