from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import chechout
from .serializers import OrderSerializer


class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self,request):

        order = chechout(request.user)
        
        serializer = OrderSerializer(order)

        return Response({
            serializer.data
        })
    
    
    