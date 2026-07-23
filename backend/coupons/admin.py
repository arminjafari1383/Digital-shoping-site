from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = [
        "code",
        "discount_type",
        "value",
        "active",
        "used_count",
    ]

    search_fields = [
        "code",
    ]