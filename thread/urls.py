from django.urls import path
from . import views


app_name = "thread"

urlpatterns = [path("", views.feed, name="feed")]
