from django.urls import path
from . import views


app_name = "thread"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("create-thread/", views.create_thread, name="create_thread"),
    path("get-thread-unit/", views.get_thread_unit, name="get_thread_unit"),
]
