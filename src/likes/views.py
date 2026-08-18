from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Like
from .serializers import LikeSerializer, LikeUserSerializer, LikedPostSerializer
from posts.models import Post

from notifications.services import create_like_notification

class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        like = serializer.save(user=self.request.user)

        post = like.post
        post.likes_count += 1
        post.save(update_fields=["likes_count"])

        create_like_notification(like)

class DeleteLikeView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(
            user=self.request.user,
        )

    def perform_destroy(self, instance):
        post = instance.post

        instance.delete()

        post.likes_count -= 1
        post.save(update_fields=["likes_count"])

class LikeListView(generics.ListAPIView):
    serializer_class = LikeUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Like.objects
            .filter(post_id=self.kwargs["post_id"])
            .select_related("user")
        )

class LikedPostListView(generics.ListAPIView):
    serializer_class = LikedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Post.objects
            .filter(
                likes__user=self.request.user,
                is_deleted=False,
            )
            .select_related("author")
            .distinct()
        )
