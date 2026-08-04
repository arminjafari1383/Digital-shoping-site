from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSeializer


class AddressListCreateView(generics.ListCreateAPIView):

    serializer_class = AddressSeializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AddressSeializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    
