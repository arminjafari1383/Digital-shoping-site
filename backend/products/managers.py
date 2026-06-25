from django.db import models
from models import Product

class ProductManger(models.Manager):

    def active(self):
        return self.filter(stock__gt=0)
    
    Product.objects.active()
    
    