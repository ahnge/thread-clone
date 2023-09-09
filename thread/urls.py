from django.urls import path
from . import views


app_name = "thread"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("following-feed/", views.following_feed, name="following_feed"),
    path("search/", views.search, name="search"),
    path("search-query/", views.search_query, name="search_query"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path("create-reply/", views.create_reply, name="create_reply"),
    # htmx form related (thread and comment)
    path(
        "thread-reply-form/<int:id>/",
        views.get_thread_reply_form,
        name="get_thread_reply_form",
    ),
    path(
        "comment-reply-form/<int:id>/",
        views.get_comment_reply_form,
        name="get_comment_reply_form",
    ),
    path("thread-form-unit/", views.get_thread_form_unit, name="get_thread_form_unit"),
    path("reply-form-unit/", views.get_reply_form_unit, name="get_reply_form_unit"),
    # htmx like features related routes
    path(
        "like-toggle/thread/<int:id>/",
        views.like_thread_toggle,
        name="like_thread_toggle",
    ),
    path(
        "like-toggle/comment/<int:id>/",
        views.like_comment_toggle,
        name="like_comment_toggle",
    ),
    # htmx detail page(thread and reply)
    path("<str:username>/threads/<int:id>/", views.get_thread, name="get_thread"),
    path("<str:username>/replies/<int:id>/", views.get_reply, name="get_reply"),
    # htmx repost threads or comments
    path(
        "repost-toggle/thread/<int:id>/",
        views.repost_thread_toggle,
        name="repost_thread_toggle",
    ),
    path(
        "repost-toggle/comment/<int:id>/",
        views.repost_comment_toggle,
        name="repost_comment_toggle",
    ),
    # htmx get likes
    path(
        "<str:username>/threads-likes/<int:id>/",
        views.get_thread_likes,
        name="get_thread_likes",
    ),
    path(
        "<str:username>/replies-likes/<int:id>/",
        views.get_reply_likes,
        name="get_reply_likes",
    ),
    # notification htmx
    path("notification/", views.notification, name="notification"),
    path("check-reddot/", views.check_reddot, name="check_reddot"),
]
