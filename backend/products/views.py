from rest_framework.generics import *
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .filters import ProductFilter
from django.core.cache import cache
from rest_framework.response import Response


class ProductListView(ListAPIView):

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

    def list(self,request,*args,**kwargs):

        cache_key = "products_list"

        data = cache.get(cache_key)

        if data is None:

            queryset = (
                Product.objects
                .select_related(
                    "category",
                    "brand",
                )
                .prefetch_related(
                    "images",
                )
            )

            queryset = self.filter_queryset(
                queryset
            )

            serializer = self.get_serializer(
                queryset,
                many=True
            )
            data = serializer.data

            cache.set(
                cache_key,
                data,
                timeout=300
            )
        return Response(data)
    
    

class ProductDetailView(
    RetrieveAPIView
):
    
    queryset = (
        Product.objects.select_related(
            "category",
            "brand",
        )
        .prefetch_related(
            "images",
        )
    )

    serializer_class = ProductSerializer

    lookup_field = 'slug'

    
