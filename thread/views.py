from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Thread


@login_required
def home(request):
    return render(request, "base.html")


@login_required
def feed(request):
    threads = Thread.objects.all()
    context = {"threads": threads}
    return render(request, "thread/feed.html", context)
