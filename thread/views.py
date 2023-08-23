from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Thread, ThreadImage


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


@login_required
def create_thread(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        for afile in request.FILES.getlist("thread_images"):
            # Save images in respective models with the links to other models
            print(afile)
        return redirect("thread:feed")
    else:
        return redirect("thread:feed")


@login_required
def get_thread_unit(request):
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "partials/_thread_unit.html")
    return redirect("thread:feed")
