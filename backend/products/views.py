from rest_framework.generics import *
from .models import *
from .serializers import *


class ProductListView(ListAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    filterset_fields = [

        'category'
    
    ]

    searcg_fields = [

        'title'

    ]

    ordering_fields = [

        'price',

        'created_at'

    ]

class ProductDetailView(
    RetrieveAPIView
):
    
    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    lookup_field = 'slug'

    
