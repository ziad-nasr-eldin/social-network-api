from django.urls import path

from .views import CreateLikeView


urlpatterns = [
    path(
        "likes/",
        CreateLikeView.as_view(),
        name="create_like",
    ),
]
