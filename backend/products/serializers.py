from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductImage

        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    images = ProductImageSerializer(
        
        many = True

    )

    class Meta:
        
        model = Product

        fields = '__all__'

        