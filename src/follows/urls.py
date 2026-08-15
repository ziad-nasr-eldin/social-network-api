from django.urls import path

from .views import CreateFollowView, DeleteFollowView


urlpatterns = [
    path(
        "follows/",
        CreateFollowView.as_view(),
        name="create_follow",
    ),
    path(
    "follows/<uuid:user_id>/",
    DeleteFollowView.as_view(),
    name="delete_follow",
),
]
