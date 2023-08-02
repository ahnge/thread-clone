from django.shortcuts import render


def feed(request):
    return render(request, "base.html")
