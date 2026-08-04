from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryser(self):

        return  (
            Notification.objects
            .filter(user=self.request.user)
            .order_by("-created_at")
        )


class MarkNotificationsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,pk):

        notification = Notification.objects.get(
            id = pk,
            user=request.user
        )

        notification.is_read = True

        notification.save(
            update_fields=["is_read"]
        )

        return Response({
            "message":"Notification marked as read."
        })



class UnreadNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        count = Notification.objects.filter(
            user = request.user,
            is_read = False
        ).count()

        return Response({
            "unread_notifications":count
        })

    