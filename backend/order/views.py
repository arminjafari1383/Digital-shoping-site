from django.db.models import Sum,Count
from django.utils import timezone
from django.db.models.functions import TruncDate,TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .services import chechout
from .serializers import OrderSerializer
from .models import Order, OrderItem
from products.models import Product,ProductVariant
from accounts.models import User
from datetime import timedelta


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
            ).aggregate(
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
            .aggregate(total=Sum("total_price"))["total"] or 0
        )

        low_stock_products = (
            ProductVariant.objects
            .filter(stock__lt=5, stock__gt=0)
            .select_related("product","color","size")

        )

        out_of_stock_products = (
            ProductVariant.objects
            .filter(stock=0)
            .select_related("product","color","size")
        )

        low_stock_data = [
            {
                "variant_id":str(item.id),
                "product":item.product.title,
                "color":item.color.name,
                "size":item.size.value,
                "stock":item.stock,
            }

            for item in low_stock_products
        ]


        out_of_stock_data = [
            {
                "variant_id":str(item.id),
                "product":item.product.title,
                "color":item.color.name,
                "size":item.size.value,
                "stock":item.stock,
            }

            for item in out_of_stock_products
        ]

        daily_sales = (
            Order.objects
            .filter(status="paid")
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(
                income=Sum("total_price"),
                orders=Count("id")
            )
            .order_by("day")
        )

        monthly_sales = (
            Order.objects
            .filter(status="paid")
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(
                income=Sum("total_price"),
                orders=Count("id")
            )
            .order_by("month")
        )

        daily_chart = [
            {
                "date": item["day"],
                "income":item["income"],
                "orders":item["orders"],
            }

            for item in daily_sales
        ]

        monthly_chart = [
            {
                "month":item["month"],
                "income":item["income"],
                "orders":item["orders"],
            }
            for item in monthly_sales
        ]


        total_users = User.objects.filter(
            date_joined__date = today
        ).count()

        month_users = User.objects.filter(
            date__joined__year = now.year,
            date_joined__month=now.month
        ).count()


        published_products = Product.objects.filter(
            status = Product.Status.PUBLISHED
        ).count()

        draft_products = Product.objects.filter(
            status = Product.Status.DRAFT
        ).count()

        first_day_this_month = now.replace(day=1)

        last_month = first_day_this_month - timedelta(days=1)

        last_month_income = (
            Order.objects.filter(
                status = "paid",
                created_at__year = last_month.year,
                created_at__month = last_month.month
            ).aggregate(
                total=Sum("total_price")
            )["total"] or 0
        )

        if last_month_income > 0:
            growth = (
                (month_income - last_month_income)
                /last_month_income
            ) * 100

        else:
            growth = 100 if month_income > 0 else 0


        return Response({

            "total_orders": total_orders,

            "paid_orders": paid_orders,

            "total_income": total_income,

            "total_products":total_products,

            "total_users":total_users,

            "latest_orders": latest_orders,

            "best_selling_products": list(best_selling),

            "today_orders": today_orders_count,

            "today_income": today_income,

            "month_orders": month_orders_count,

            "month_income": month_income,

            "low_stock_products": low_stock_data,

            "out_of_stock_products": out_of_stock_data,

            "daily_sales":daily_chart,

            "monthly_sales":monthly_chart,

            "today_users": today_users,

            "month_users": month_users,

            "published_products":published_products,

            "draft_products":draft_products,

            "last_month_income":last_month_income,

            "sales_growth_percent":round(growth,2),
            
        })

    

    