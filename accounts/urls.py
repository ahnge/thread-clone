from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_threads,
    profile_replies,
    profile_reposts,
    follow_toggle,
)

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/<str:username>/", profile_view, name="profile"),
    path("profile/<str:username>/threads/", profile_threads, name="profile_threads"),
    path("profile/<str:username>/replies/", profile_replies, name="profile_replies"),
    path("profile/<str:username>/reposts/", profile_reposts, name="profile_reposts"),
    # htmx follow toggle
    path(
        "follow-toggle/profile/<int:id>/",
        follow_toggle,
        name="follow_toggle",
    ),
]
