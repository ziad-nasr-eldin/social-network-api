from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import Post, Media
from .serializers import PostSerializer, MediaSerializer
from .permissions import IsAuthorOrReadOnly


class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Post.objects
            .filter(is_deleted=False)
            .select_related("author", "original_post")
            .prefetch_related("media")
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

