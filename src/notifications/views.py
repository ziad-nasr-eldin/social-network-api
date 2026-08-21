from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Notification.objects
            .filter(recipient=self.request.user)
            .select_related(
                "actor",
                "post",
                "comment",
            )
            .order_by("-created_at")
        )

class MarkNotificationAsReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
        )

    def update(self, request, *args, **kwargs):
        notification = self.get_object()

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        serializer = self.get_serializer(notification)

        return Response(serializer.data)