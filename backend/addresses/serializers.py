from rest_framework import serializers
from .models import Address

class AddressSeializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created_at",
        )

        