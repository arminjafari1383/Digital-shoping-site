from django.urls import path
from .views import *

urlpatterns = [
    path('',CartDetailView.as_view()),
    path('add/',AddToCartView.as_view()),
    path('remove/',RemoveFromCartView.as_view()),
    path('update/',UpdateCartItemView.as_view()),
]

