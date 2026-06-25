from django.db import models
import uuid
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name
    
class Product(models.Model):

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()
    price = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    discount_price = models.DecimalField(

        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    stock = models.PositiveIntegerField()

    category = models.ForeignKey(

        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_at = models.DateTimeField(
        auto_now_add=True

    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
        
class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
    image = models.ImageField(
        upload_to='products/'
    )

    is_primary = models.BooleanField(
        default = False
    )