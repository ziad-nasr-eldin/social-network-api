from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Follow
from .serializers import FollowSerializer, FollowerSerializer


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


class DeleteFollowView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(
            follower=self.request.user,
            following_id=self.kwargs["user_id"],
        )

    def perform_destroy(self, instance):
        follower = instance.follower
        following = instance.following

        instance.delete()

        follower.following_count -= 1
        following.followers_count -= 1

        follower.save(update_fields=["following_count"])
        following.save(update_fields=["followers_count"])


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Follow.objects
            .filter(following_id=self.kwargs["user_id"])
            .select_related("follower")
        )