from rest_framework import serializers
from .models import Cart,CartItem


class CartItemSerializer(serializers.ModelSerializer):

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','variant','quantity','total_price']
    

    def get_total_price(self,obj):
        return obj.total_price()
    

class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many = True,read_only = True)

    class Meta:
        model = Cart
        fields = ['id','user','session_id','items']

