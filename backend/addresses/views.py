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

        is_default = serializer.validated_date.get(
            "is_dafault",
            False
        )

        if is_default:
            Address.objects.filter(
                user = self.request.user,
                is_default=True
            ).update(is_default=False)

        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AddressSeializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_update(self,serializer):
        is_default = serializer.validated_data.get(
            "is_default",
            False
        )

        if is_default:
            Address.objects.filter(
                user = self.request.user,
                is_default=True
            ).exclude(
                id=self.get_object().id
            ).update(is_default=False)
        serializer.save()

        
    
