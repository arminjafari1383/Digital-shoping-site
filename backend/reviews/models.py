from django.db import models

from django.conf import settings

class Review(models.Model):

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ("product","user")

    def __str__(self):
        return f"{self.user} - {self.product}"

    
