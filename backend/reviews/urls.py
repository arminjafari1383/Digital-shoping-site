from django.urls import path

from .views import (ReviewListCreateView,ReviewDetailView,)

urlpatterns = [
    path("products/<uuid:product_id>/reviews/",ReviewListCreateView.as_view(),name="product-reviews",),
    path("reviews/<uuid:pk>/",ReviewDetailView.as_view(),name="review-detail",),
]