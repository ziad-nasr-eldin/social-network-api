from django.contrib import admin
from .models import Comment
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "author", "post", "short_content",
        "is_deleted", "created_at",
    )
    list_filter = ("is_deleted", "created_at")
    search_fields = ("content", "author__username", "post__id")
    autocomplete_fields = ("author", "post")
    ordering = ("-created_at",)

    @admin.display(description="Content")
    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
