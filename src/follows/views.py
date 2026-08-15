from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Follow
from .serializers import FollowSerializer


class CreateFollowView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follow = serializer.save(follower=self.request.user)

        follower = follow.follower
        following = follow.following

        follower.following_count += 1
        following.followers_count += 1

        follower.save(update_fields=["following_count"])
        following.save(update_fields=["followers_count"])

