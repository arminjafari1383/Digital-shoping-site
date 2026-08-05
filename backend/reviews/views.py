from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError

from .models import Review
from .serializers import ReviewSerializer
from products.models import Product
from django.shortcuts import get_object_or_404
from products.models import Product




class ReviewListCreateView(generics.ListCreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        return Review.objects.filter(
            product_id=product_id
        ).select_related(
            "user",
            "product"
        )

    def perform_create(self,serializer):

        product = get_object_or_404(
            Product,
            id=self.kwargs["product_id"]
        )
        serializer.save(
            user=self.request.user,
            product=product
        )

        if Review.objects.filter(
            product=product,
            user=self.request.user
        ).exists():

            raise ValidationError(
                {
                    "detail":"You have already reviewed this product."
                }
            )

        serializer.save(
            user = self.request.user,
            product=product
        )

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.select_related(
        "user",
        "product"
    )

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self,serializer):
        if serializer.instance.user != self.request.user:

            raise ValidationError(
                {
                    "detail":"You cannot edit this review."
                }
            )

        serializer.save()


    def perform_destroy(self,instance):

        if instance.user != self.request.user:

            raise ValidationError(
                {
                    "detail":"You cannot delete this review."
                }
            )
        instance.delete()

