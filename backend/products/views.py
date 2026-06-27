from rest_framework.generics import *
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend



class ProductListView(ListAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]

    filterset_fields = [

        'category',
        'brand',
        'status'
    
    ]

    search_fields = [

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

    
