from django.urls import path

from .views import NotificationListView, MarkNotificationAsReadView, UnreadNotificationCountView


urlpatterns = [
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notification_list",
    ),
    path(
        "notifications/<uuid:pk>/read/",
        MarkNotificationAsReadView.as_view(),
        name="mark_notification_as_read",
    ),
    path(
        "notifications/unread-count/",
        UnreadNotificationCountView.as_view(),
        name="unread_notification_count",
    ),
]