import uuid

from django.db import models

class Payment(models.Model):
    
    class Status(models.TextChoices):

        PENDING = "pending","Pending"

        SUCCESS = "success","Success"

        FAILED = "failed" , "Faield"

    
    id = models.UUIDField(
        primary_key=True,
        default = uuid.uuid4,
        editable=False
    )

    order = models.OneToOneField(
        "order.Order",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    authority = models.CharField(
        max_length=200,
        blank=True
    )

    ref_id = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.id)
    
    