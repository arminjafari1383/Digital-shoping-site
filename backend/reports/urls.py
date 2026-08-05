from django.urls import path
from .views import OrderReportView,ProductSalesReportView

urlpatterns = [
    path("orders/",OrderReportView.as_view(),name="order-report"),
    path("products/", ProductSalesReportView.as_view(),name="product-sales-report"),
]