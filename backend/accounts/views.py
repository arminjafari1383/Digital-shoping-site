from rest_framework.generics import CreateAPIView,RetrieveAPIView
from .serializers import RegisterSerializer,ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    premission_classes = [IsAuthenticated]

    def post(self, request):
        
        try:
            token = request.data["refresh"]
            refresh = RefreshToken(token)
            refresh.blacklist()
            return Response(status=205)
        
        except:

            return Response(
                status=400
            )