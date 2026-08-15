from django.urls import path

from .views import CreateFollowView


urlpatterns = [
    path(
        "follows/",
        CreateFollowView.as_view(),
        name="create_follow",
    ),
]
