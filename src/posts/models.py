import uuid
from django.conf import settings
from django.db import models

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    content = models.TextField(max_length=500)

    # Original post for repost functionality
    original_post = models.ForeignKey(
        "self",
        related_name="reposts",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    reposts_count = models.PositiveIntegerField(default=0)

    # Soft delete
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            # Optimized for user profile timeline
            models.Index(fields=["author", "-created_at"]),
            # Optimized for global feed queries
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Post by {self.author}"


class Media(models.Model):
    IMAGE = "image"
    VIDEO = "video"

    TYPE_CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post,
        related_name="media",
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="posts/%Y/%m/")
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Display order for multiple media files
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.media_type} - {self.post_id}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    content = models.TextField(max_length=500)

    # Soft delete flag
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"
