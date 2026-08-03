from django.urls import path
from .views import CheckoutView,DashboardView

urlpatterns = [
    path("checkout/",CheckoutView.as_view()),
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
]