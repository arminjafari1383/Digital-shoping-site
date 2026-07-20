from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart
from rest_framework.exceptions import ValidationError
from django.db.models import F



# why use transaction.atomic ?
# suppose that 1 - order create 2 - product inventory is running low 
# if didn't transaction datebse destroied
@transaction.atomic
def chechout(user):
    
    # decrease query
    cart  = (
         Cart.objects
         .prefetch_related(
              "items__product"
         )
         .get(user=user)
    )
    # if the shopping cart was empty
    if not cart.items.exists():
        raise VadlidationError({
            "cart":"Your cart is empty."
        })
    
    # create order
    order = Order.objects.create(
        user = user
    )

    # total price
    total_price = 0

    # loop on cart items
    for item in cart.items.all():
        # check cash
        if item.product.stock <= 0:
                raise VadlidationError({
                    "stock":f"{item.product.title} is out of stock."
                })
            
    
        # create orderitem
        OrderItem.objects.create(
            order = order,

            product = item.product,

            quantity = item.quantity,

            price = item.product.discount_price or item.product.price
        )

        # reduce cash
        item.product.stock = F("stock") - item.quantity

        item.product.save(update_fields=["stock"])

        item.product.refresh_from_db()

        # sum costs

        total_price += item.quantity * item.product.price

    # save costs
    
    order.total_price = total_price
    
    order.save()

    # Empty cart

    cart.items.all().delete()

    # return order

    return {
         "order":order,
         "total":total_price
    }

