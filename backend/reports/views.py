from django.db.models import Sum,Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from order.models import Order,OrderItem


class OrderReportView(APIView):

    permission_classes = [IsAdminUser]

    def get(self,request):
        report = (
            Order.objects
            .values("status")
            .annotate(
                total_orders = Count("id"),
                total_income=Sum("total_price")
            )
        )

        return Response(report)


class ProductSalesReportView(APIView):

    permission_classes = [IsAdminUser]

    def get(self,request):

        report = (
            OrderItem.objects
            .values("product__title")
            .annotate(
                sold=Sum("quantity"),
                revenue = Sum("price")
            )
            .order_by("-sold")
        )

        return Response(report)

    