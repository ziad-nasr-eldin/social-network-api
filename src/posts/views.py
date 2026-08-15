from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import Post, Media
from .serializers import PostSerializer, MediaSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import FeedPagination


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user

        following_ids = user.following_set.values_list(
            "following_id",
            flat=True,
        )

        return (
            Post.objects
            .filter(
                author_id__in=list(following_ids) + [user.id],
                is_deleted=False,
            )
            .select_related("author")
            .prefetch_related("media")
            .order_by("-created_at")
        )


class UpdatePostView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)

class RetrievePostView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Post.objects
            .filter(is_deleted=False)
            .select_related("author", "original_post")
            .prefetch_related("media")
        )

class DeletePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"message": "Post deleted successfully."},
            status=status.HTTP_200_OK,
        )

class UploadMediaView(generics.CreateAPIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.validated_data["post"]

        if post.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You do not have permission to upload media to this post."
            )

        serializer.save()


class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        following_ids = user.following_set.values_list(
            "following_id",
            flat=True,
        )

        return (
            Post.objects
            .filter(
                author_id__in=list(following_ids) + [user.id],
                is_deleted=False,
            )
            .select_related("author")
            .prefetch_related("media")
            .order_by("-created_at")
        )