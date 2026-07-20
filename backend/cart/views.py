from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart
from products.models import ProductVariant
from .serializers import CartSerializer,CartItemSerializer
from django.shortcuts import get_object_or_404

#helper for get cart
def get_or_create_cart(request):
    if request.user.is_authenticated:

        cart,created = Cart.objects.get_or_create(user=request.user)

    else:

        session_id = request.session.session_key

        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart,created = Cart.objects.get_or_create(session_id=session_id)

    return cart



# add to cart
class AddToCartView(APIView):
    
    def post(self, request):    
        cart = get_or_create_cart(request)

        variant_id = request.data.get('variant_id')

        quantity = int(request.data.get('quantity',1))

        variant = get_object_or_404(
            ProductVariant,
            id = variant_id
        )

        product = Product.objects.get(id=product_id)

        item,created = cart.items.get_or_create(
            variant=variant
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        
        item.save()

        return Response(CartSerializer(cart).data)
    

#Remove item

class RemoveFromCartView(APIView):
    def post(self,request):
        
        cart = get_or_create_cart(request)

        item_id = request.data.get('item_id')

        cart.items.filter(id=item_id).delete()

        return Response(CartSerializer(cart).data)
    

#Update quantity

class UpdateCartItemView(APIView):

    def post(self, request):

        cart = get_or_create_cart(request)

        item_id = request.data.get('item_id')

        quantity = int(request.data.get('quantity'))

        item = cart.items.get(id=item_id)
        item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data)

# Get Cart

class CartDetailView(APIView):
    
    def get(self,request):

        cart = get_or_create_cart(request)

        return Response(CartSerializer(cart).data)
        