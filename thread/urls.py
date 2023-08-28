from django.urls import path
from . import views


app_name = "thread"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path("create-reply/", views.create_reply, name="create_reply"),
    # htmx
    path("get-thread-unit/", views.get_thread_form_unit, name="get_thread_form_unit"),
    path(
        "<str:username>/get-reply-form/<int:id>/",
        views.get_reply_form,
        name="get_reply_form",
    ),
    path("get-reply-form-unit/", views.get_reply_form_unit, name="get_reply_form_unit"),
]
