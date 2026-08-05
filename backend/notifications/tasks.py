from celery import shared_task
from .services import create_notification
from .models import Notification

from accounts.models import User

@shared_task
def send_notification_task(
    user_id,
    title,
    message,
    notification_type
):
    user = User.objects.get(
        id=user_id
    )

    create_notification(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )
    