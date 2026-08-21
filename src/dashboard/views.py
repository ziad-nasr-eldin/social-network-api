from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        posts_count = user.posts.filter(
            is_deleted=False,
        ).count()

        likes_received = (
            user.posts.filter(
                is_deleted=False,
            ).aggregate(
                total=Sum("likes_count"),
            )["total"]
            or 0
        )

        comments_received = (
            user.posts.filter(
                is_deleted=False,
            ).aggregate(
                total=Sum("comments_count"),
            )["total"]
            or 0
        )

        return Response({
            "posts_count": posts_count,
            "followers_count": user.followers_count,
            "following_count": user.following_count,
            "likes_received": likes_received,
            "comments_received": comments_received,
        })