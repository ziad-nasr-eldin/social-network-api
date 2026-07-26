from django.contrib import admin
from .models import Post, Media


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1
    fields = ("file", "media_type", "order")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id", "author", "short_content", "likes_count",
        "comments_count", "reposts_count", "deleted_status", "created_at",
    )
    list_filter = ("is_deleted", "created_at")
    search_fields = ("content", "author__username")
    autocomplete_fields = ("author", "original_post")
    readonly_fields = ("likes_count", "comments_count", "reposts_count")
    inlines = [MediaInline]
    ordering = ("-created_at",)

    @admin.display(description="Content", ordering="content")
    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")

    @admin.display(description="Deleted", boolean=True)
    def deleted_status(self, obj):
        return obj.is_deleted


