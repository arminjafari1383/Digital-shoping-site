from rest_framework import serializers
from .models import Wishlist



class wishlistSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source = "product.title",
        read_only = True

    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits = 10,
        decimal_places = 2,
        read_only = True
    )

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "product",
            "product_title",
            "product_price",
            "created_at",
        ]

        