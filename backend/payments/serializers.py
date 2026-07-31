from rest_framework import serializers
from .models import Payment

class PaymentSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "status",
            "authority",
            "ref_id",
            "paid_at",
        )

        