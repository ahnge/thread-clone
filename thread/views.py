from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Thread


@login_required
def home(request):
    return redirect("thread:feed")


@login_required
def feed(request):
    threads = Thread.objects.all()
    context = {"threads": threads}
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/feed.html", context)
    return render(request, "thread/f_feed.html", context)
