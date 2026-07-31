from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "created_at",
    )
    list_filter = (
        "created_at",
    )
    search_fields = (
        "user__username",
        "post__id",
    )
    autocomplete_fields = (
        "user",
        "post",
    )
    ordering = (
        "-created_at",
    )
