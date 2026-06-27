from django.db import models
import uuid
from django.utils.text import slugify
from .managers import ProductManager


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

class Brand(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )
    
    slug = models.SlugField(
        unique=True
    )

    logo = models.ImageField(
        upload_to='brands/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(
        max_length=50
    )
    
    code = models.CharField(
        max_length=7
    )

    def __str__(self):
        return self.name

class Size(models.Model):
    
    value = models.CharField(
        max_length=30
    )

    def __str__(self):
        return self.value
    

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft','Draft'
        PUBLISHED = 'published','Published'
    
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        )
    
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

   

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    status = models.CharField(

        max_length = 20,
        choices = Status.choices,
        default = Status.DRAFT

    )
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args,**kwargs)

    objects = ProductManager()
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at'])
        ]
    
    



class ProductVariant(models.Model):
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE
    )

    stock = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sku = models.CharField(
        max_length=100,
        unique = True
    )

    class Meta:
        unique_together = (
            'product',
            'color',
            'size'
        )

    def __str__(self):
        return (
            f"{self.product.title}"
            f" - "
            f"{self.color.name}"
        )

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



