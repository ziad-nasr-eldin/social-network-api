from .views import CreateLikeView, DeleteLikeView, LikeListView


urlpatterns = [
    path(
        "likes/",
        CreateLikeView.as_view(),
        name="create_like",
    ),
    path(
        "likes/<uuid:pk>/",
        DeleteLikeView.as_view(),
        name="delete_like",
    ),
    path(
        "posts/<uuid:post_id>/likes/",
        LikeListView.as_view(),
        name="post_likes",
    ),
    path(
        "likes/my-posts/",
        LikedPostListView.as_view(),
        name="liked_posts",
    ),
]
