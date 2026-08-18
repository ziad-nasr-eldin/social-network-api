from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly

from notifications.services import create_comment_notification


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(
            author=self.request.user
        )

        post = comment.post
        post.comments_count += 1
        post.save(update_fields=["comments_count"])
    
        create_comment_notification(comment)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Comment.objects
            .filter(
            post_id=self.kwargs["post_id"],
            is_deleted=False,
        )
        .select_related("author")
    )

class RetrieveCommentView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Comment.objects
            .filter(is_deleted=False)
            .select_related("author", "post")
        )

class UpdateCommentView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        return (
            Comment.objects
            .filter(is_deleted=False)
            .select_related("author", "post")
        )

class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            author=self.request.user,
            is_deleted=False,
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

        post = instance.post
        post.comments_count -= 1
        post.save(update_fields=["comments_count"])