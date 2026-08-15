from django.urls import path

from .views import CreateFollowView, DeleteFollowView, FollowersListView, FollowingListView


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
    path(
    "users/<uuid:user_id>/following/",
    FollowingListView.as_view(),
    name="following_list",
    ),
]
