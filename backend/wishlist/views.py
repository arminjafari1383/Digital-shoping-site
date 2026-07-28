from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Wishlist
from .serializers import wishlistSerializer

from products.models import Product

class AddToWishlistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")

        product = get_object_or_404(
            Product,
            id = product_id
        )

        if Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists():
            return Response(
                {
                    "message":"Product already exists in wishlist."
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        wishlist = Wishlist.objects.create(
            user = request.user,
            product=product
        )

        serializer = wishlistSerializer(wishlist)


        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )


class WishlistListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        wishlist = (
            Wishlist.objects
            .select_related("product")
            .filter(user=request.user)
        )

        serializer = wishlistSerializer(
            wishlist,
            many = True
        )

        return Response({
            "count":wishlist.count(),
            "results":serializer.data
        })


class RemoveWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request,product_id):

        item = get_object_or_404(
            Wishlist,
            user = request.user,
            product_id=product_id
        )

        item.delete()

        return Response(
            {"message":"Removed successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    