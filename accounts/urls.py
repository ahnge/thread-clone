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
    profile_followers,
    profile_following,
    profile_edit,
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
    # htmx followers and followings get
    path(
        "profile/<str:username>/followers/", profile_followers, name="profile_followers"
    ),
    path(
        "profile/<str:username>/following/", profile_following, name="profile_following"
    ),
    # edit profile
    path("profile/<int:id>/edit/", profile_edit, name="profile_edit"),
]
