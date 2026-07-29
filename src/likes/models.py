from django.db import models

import uuid

from django.conf import settings

from posts.models import Post


class Like(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="likes",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_like",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "post"]),
            models.Index(fields=["post", "user"]),
        ]

    def __str__(self):
        return f"{self.user} liked {self.post.id}"
