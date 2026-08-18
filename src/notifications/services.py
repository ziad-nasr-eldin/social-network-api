from .models import Notification


def create_like_notification(like):
    post = like.post

    if post.author == like.user:
        return

    Notification.objects.create(
        recipient=post.author,
        actor=like.user,
        notification_type=Notification.LIKE,
        post=post,
    )