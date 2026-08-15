from rest_framework import serializers

from .models import Like
from posts.models import Post

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "post",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )

class LikeUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Like
        fields = (
            "username",
            "created_at",
        )

class LikedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "likes_count",
            "comments_count",
            "reposts_count",
            "created_at",
        )
