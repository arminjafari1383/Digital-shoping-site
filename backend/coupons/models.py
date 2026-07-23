from django.db import models


class Coupon(models.Model):

    class DiscountType(models.TextChoices):
        
        PERCENT = "percent","Percent"
        FIXED = "fixed","Fixed"

    code = models.CharField(
        max_length=30,
        unique=True
    ) 

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    min_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    usage_limit = models.PositiveIntegerField(
        default=1
    )

    used_count = models.PositiveIntegerField(
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    def __str__(self):
        return self.code
    

