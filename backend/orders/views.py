from rest_framework.views import APIView
from rest_framework.response import Response

class CheckoutView(APIView):
    
    def post(self,request):

        """
        compelte next time
        
        """

        return Response({
            "message":"Checkout API"
        })
    
    