from rest_framework import serializers

from .models import *

from wishlist.models import Wishlist

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductImage

        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):

    is_in_wishlist = serializers.SerializerMethodField()

    category = CategorySerializer()

    images = ProductImageSerializer(
        
        many = True

    )

    class Meta:
        
        model = Product

        fields = '__all__'

    def get_is_in_wishlist(self,obj):

        request = self.context.get("request")

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        return Wishlist.objects.filter(
            user=request.user,
            product=obj
        ).exists()
    

        