from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True

    )

    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    
    cart = models.ForeignKey(
        Cart,
        on_delete = models.CASCADE,
        related_name='items'
    )

    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.variant.price
    
