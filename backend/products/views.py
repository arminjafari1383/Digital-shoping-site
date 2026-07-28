from rest_framework.generics import *
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

from .filters import ProductFilter



class ProductListView(ListAPIView):

    queryset = (Product.objects.select_related(
        "category",
        "brand",
    )
    .prefetch_related(
        "images",
    )

    )

    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,

        SearchFilter,

        OrderingFilter,

        ]

    filterset_fields = ProductFilter

    search_fields = [

        'title',

        'description',

    ]

    ordering_fields = [

        'price',

        'created_at'

    ]

    ordering = [
        "-created_at"
    ]

    

class ProductDetailView(
    RetrieveAPIView
):
    
    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    lookup_field = 'slug'

    
