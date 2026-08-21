from django.db.models import Sum

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.serializers import PostSerializer


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        posts = (
            user.posts
            .filter(is_deleted=False)
            .select_related("author")
            .prefetch_related("media")
            .order_by("-created_at")[:5]
        )

        posts_count = user.posts.filter(
            is_deleted=False,
        ).count()

        likes_received = (
            user.posts
            .filter(is_deleted=False)
            .aggregate(total=Sum("likes_count"))["total"]
            or 0
        )

        comments_received = (
            user.posts
            .filter(is_deleted=False)
            .aggregate(total=Sum("comments_count"))["total"]
            or 0
        )

        return Response({
            "stats": {
                "posts_count": posts_count,
                "followers_count": user.followers_count,
                "following_count": user.following_count,
                "likes_received": likes_received,
                "comments_received": comments_received,
            },
            "recent_posts": PostSerializer(
                posts,
                many=True,
                context={"request": request},
            ).data,
        })