from django.urls import path

from .views import (
    NotificationListView,
    MarkNotificationsReadView,
    UnreadNotificationCountView,
)

urlpatterns = [
    path("",NotificationListView.as_view(),name="notification-list",),
    path("<uuid:pk>/read/",MarkNotificationsReadView.as_view(),name="notification-read",),
    path("unread-count/",UnreadNotificationCountView.as_view(),name="notification-count",),
]