from django.db.models import Sum,Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .services import chechout
from .serializers import OrderSerializer
from .models import Order, OrderItem
from products.models import Product
from accounts.models import User
from django.utils import timezone



class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self,request):

        order = chechout(request.user)
        
        serializer = OrderSerializer(order)

        return Response({
            serializer.data
        })
    


class DashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self,request):

        total_orders = Order.objects.count()

        paid_orders = Order.objects.filter(
            status = "paid"
        ).count()

        total_income = (
            Order.objects.filter(
                status="paid"
            ).aaggregate(
                total = Sum("total_price")
            )["total"] or 0
        )

        total_products = Product.objects.count()

        total_users = User.objects.count()

        latest_orders = (
            Order.objects
            .select_related("user")
            .order_by("-created_at")[:5]
            .values(
                "id",
                "user__email",
                "total_price",
                "status",
                "created_at",
            )
        )

        best_selling = (
            OrderItem.objects
            .values("product__title")
            .annotate(
                sold = Sum("quantity")
            )

            .order_by("-sold")[:10]
        )

        today = timezone.now().date()

        today_orders = Order.objects.filter(
            created_at__date = today
        )

        today_orders_count = today_orders.count()

        today_income = (

            today_orders.filter(status="paid")
            .aggregate(total=Sum("total_price"))["total"] or 0
        )

        now = timezone.now()

        month_orders = Order.objects.filter(
            created_at__year = now.year,
            created_at__month = now.month
        )

        month_orders_count = month_orders.count()

        month_income = (
            month_orders.filter(status="paid")
            .aaggregate(total=Sum("total_price"))["total"] or 0
        )

        return Response({

            "total_orders": total_orders,

            "paid_orders": paid_orders,

            "total_income": total_income,

            "total_products":total_products,

            "total_users":total_users,

            "latest_orders": latest_orders,

            "best_selling_products": best_selling,

            "today_orders": today_orders_count,

            "today_income": today_income,

            "month_orders": month_orders_count,

            "month_income": month_income,
        })

    

    