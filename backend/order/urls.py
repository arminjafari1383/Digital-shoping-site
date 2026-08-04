from django.urls import path
from .views import CheckoutView,DashboardView,UpdateOrderStatusView

urlpatterns = [
    path("checkout/",CheckoutView.as_view()),
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
    path("orders/<uuid:order_id>/status/",UpdateOrderStatusView.as_view(),name="update-order-status",),
]