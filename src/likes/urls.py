from .views import CreateLikeView, DeleteLikeView


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
]
