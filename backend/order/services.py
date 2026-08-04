from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart
from rest_framework.exceptions import ValidationError
from django.db.models import F
from notifications.services import create_notification
from notifications.models import Notification



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
        raise ValidationError({
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
        variant = item.variant

        if variant.stock < item.quantity:
            raise ValidationError({
                "stock":f"{variant.product.title} does not have enough stock"
            })
            
    
        # create orderitem
        OrderItem.objects.create(
            order = order,

            product = item.product,

            variant = variant,

            quantity = item.quantity,

            price = variant.price
        )

        # reduce cash
        variant.product.stock = F("stock") - item.quantity

        variant.product.save(update_fields=["stock"])

        variant.product.refresh_from_db()

        # sum costs

        total_price += item.quantity * item.product.price

    # save costs
    
    order.total_price = total_price
    
    order.save()

    # Empty cart

    cart.items.all().delete()

    create_notification(
        user = order.user,
        title="Order Created",
        message=f"Your order #{order.id} has been created successfully.",
        notification_type=Notification.Type.ORDER,
    )
    # return order

    return {
         "order":order,
         "total":total_price
    }

