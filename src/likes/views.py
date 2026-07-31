from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Like
from .serializers import LikeSerializer


class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
    like = serializer.save(user=self.request.user)

    post = like.post
    post.likes_count += 1
    post.save(update_fields=["likes_count"])
