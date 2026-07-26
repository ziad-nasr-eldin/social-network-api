from django.urls import path

from .views import (
    CommentListView,
    CreateCommentView,
    RetrieveCommentView,
    UpdateCommentView,
)

urlpatterns = [
    path(
        "posts/<uuid:post_id>/comments/",
        CommentListView.as_view(),
        name="post_comments",
    ),
    path(
        "comments/",
        CreateCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "comments/<uuid:pk>/",
        RetrieveCommentView.as_view(),
        name="retrieve_comment",
    ),
    path(
        "comments/<uuid:pk>/update/",
        UpdateCommentView.as_view(),
        name="update_comment",
    ),

]
