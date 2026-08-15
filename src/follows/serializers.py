from rest_framework import serializers

from .models import Follow


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="follower.username",
    )

    class Meta:
        model = Follow
        fields = (
            "username",
            "created_at",
        )


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="following.username",
    )

    class Meta:
        model = Follow
        fields = (
            "username",
            "created_at",
        )