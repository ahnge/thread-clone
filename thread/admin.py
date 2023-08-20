from django.contrib import admin
from .models import Thread, ThreadImage, Like, Repost, Comment, CommentImage, Follow


# Define an Inline for ThreadImages
class ThreadImageInline(admin.TabularInline):
    model = ThreadImage


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ThreadImageInline]
    list_display = ["threader", "content", "created_at"]
    list_filter = ["threader"]
    search_fields = ["content"]


class CommentImageInline(admin.TabularInline):
    model = CommentImage


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentImageInline]
    list_display = ["user", "content", "created_at"]
    list_filter = ["user"]
    search_fields = ["content"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user", "thread", "created_at"]
    list_filter = ["user"]


@admin.register(Repost)
class RepostAdmin(admin.ModelAdmin):
    list_display = ["user", "thread", "created_at"]
    list_filter = ["user"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "followed", "created_at"]
    list_filter = ["follower"]
