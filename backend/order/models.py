import uuid
from django.db import models
from django.conf import settings

class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending","Pending"
        PAID = "paid","Paid"
        SHIPPED = "shipped","Shipped"
        DELIVERED = "delivered","Delivered"
        CANCELED = "canceled","Canceled"

    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="order"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)
    

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT # if product apply it couldn't delete it 
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def get_total(self):
        return self.quantity * self.price
    
    def _str__(self):
        return self.product.title
    
