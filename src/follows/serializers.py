from rest_framework import serializers

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            "id",
            "following",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )
