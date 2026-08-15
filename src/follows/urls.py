from django.urls import path

from .views import CreateFollowView, DeleteFollowView, FollowersListView


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
    path(
    "users/<uuid:user_id>/followers/",
    FollowersListView.as_view(),
    name="followers_list",
    ),
]
