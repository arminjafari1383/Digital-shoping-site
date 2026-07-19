from rest_framework import seializers
from .models import Order,OrderItem

class OrderItemSerializer(seializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(seializers.ModelSerializer):
    
    items = OrderItemSerializer(
        many = True,
        read_only = True
    )

    class Meta:
        model = Order
        fields = "all"

        