import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):
    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"

    TYPE_CHOICES = [
        (LIKE, "Like"),
        (COMMENT, "Comment"),
        (FOLLOW, "Follow"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE,
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_notifications",
        on_delete=models.CASCADE,
    )

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )

    post = models.ForeignKey(
        "posts.Post",
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    comment = models.ForeignKey(
        "comments.Comment",
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=["recipient", "-created_at"],
            ),
            models.Index(
                fields=["recipient", "is_read"],
            ),
        ]