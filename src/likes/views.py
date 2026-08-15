from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Like
from .serializers import LikeSerializer, LikeUserSerializer


class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
    like = serializer.save(user=self.request.user)

    post = like.post
    post.likes_count += 1
    post.save(update_fields=["likes_count"])


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
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Like.objects
            .filter(post_id=self.kwargs["post_id"])
            .select_related("user")
        )
