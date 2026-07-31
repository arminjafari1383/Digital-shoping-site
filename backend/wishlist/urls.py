from django.urls import path

from .views import(
    AddToWishlistView,
    WishlistListView,
    RemoveWishlistView,
)

urlpatterns = [
    path("add",AddToWishlistView.as_view(),name="wishlist-add"),
    path("",WishlistListView.as_view(),name="wishlist-list"),
    path("remove/<uuid:product_id>/",RemoveWishlistView.as_view(),name="wishlist-remove"),
]