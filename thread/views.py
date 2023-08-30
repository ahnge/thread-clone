from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Thread, Comment
from .utils import (
    create_thread_post,
    create_thread_images,
    create_cmt,
    create_cmt_images,
)


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
        content_list = request.POST.getlist("content")
        image_count_list = request.POST.getlist("image_count")
        image_list = request.FILES.getlist("thread_images")

        # Ensure thred content and thread images are not both empty.
        if len(content_list[0]) == 0 and int(image_count_list[0]) == 0:
            messages.warning(
                request, "You have to provide some content to create thread."
            )
            return redirect("thread:feed")
        # One unit case, just create a thread
        if len(content_list) == 1:
            # create thread
            thread = create_thread_post(content_list[0], request.user)
            create_thread_images(image_list, thread)
        # Two unit case, create thread and create comment
        if len(content_list) == 2:
            # create thread
            thread = create_thread_post(content_list[0], request.user)
            right = int(image_count_list[0])
            create_thread_images(image_list[:right], thread)
            # create comment
            comment = create_cmt(content_list[1], request.user, thread)
            left = int(image_count_list[0])
            right = left + int(image_count_list[1])
            create_cmt_images(image_list[left:right], comment)
        # More thatn two units, create thread, comment and child cmts
        if len(content_list) > 2:
            # create thread
            thread = create_thread_post(content_list[0], request.user)
            right = int(image_count_list[0])
            create_thread_images(image_list[:right], thread)
            # create parent comment
            comment = create_cmt(content_list[1], request.user, thread)
            left = int(image_count_list[0])
            right = left + int(image_count_list[1])
            create_cmt_images(image_list[left:right], comment)
            # create child comments
            i = 2
            while i < len(content_list):
                child_cmt = create_cmt(
                    content_list[i], request.user, thread, parent_comment=comment
                )
                left = 0
                for j in range(i):
                    left += int(image_count_list[j])
                right = left + int(image_count_list[i])
                create_cmt_images(image_list[left:right], comment=child_cmt)
                i += 1

        messages.success(request, "Thread created successfully.")
        return redirect("thread:feed")
    else:
        return redirect("thread:feed")


@login_required
def get_thread_form_unit(request):
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "partials/htmx/_thread_form_unit.html")
    return redirect("thread:feed")


@login_required
def get_reply_form(request, username, id):
    if request.META.get("HTTP_HX_REQUEST"):
        is_cmt = request.GET.get("is_cmt")[0]
        if int(is_cmt) == 1:
            post = get_object_or_404(Comment, pk=id)
        else:
            post = get_object_or_404(Thread, pk=id)
        context = {"post": post}
        return render(request, "partials/htmx/_reply_form.html", context)
    return redirect("thread:feed")


@login_required
def get_reply_form_unit(request):
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "partials/htmx/_reply_form_unit.html")
    return redirect("thread:feed")


@login_required
def create_reply(request):
    if request.method == "POST":
        content_list = request.POST.getlist("content")
        image_count_list = request.POST.getlist("image_count")
        image_list = request.FILES.getlist("reply_images")
        thread_id = request.POST.get("thread_id")
        comment_id = request.POST.get("comment_id")

        thread = get_object_or_404(Thread, pk=thread_id)
        parent_comment = None
        if comment_id:
            parent_comment = get_object_or_404(Comment, pk=comment_id)

        # Ensure thred content and thread images are not both empty.
        if len(content_list[0]) == 0 and int(image_count_list[0]) == 0:
            messages.warning(
                request, "You have to provide some content to create reply."
            )
            return redirect("thread:feed")
        # One comment case
        cmt = create_cmt(
            content=content_list[0],
            user=request.user,
            thread=thread,
            parent_comment=parent_comment,
        )
        create_cmt_images(
            image_list=image_list[: int(image_count_list[0])], comment=cmt
        )
        # More than one comment case
        if len(content_list) > 1:
            i = 1
            while i < len(content_list):
                child_cmt = create_cmt(
                    content=content_list[i],
                    user=request.user,
                    thread=thread,
                    parent_comment=cmt,
                )
                left = 0
                for j in range(i):
                    left += int(image_count_list[j])
                right = left + int(image_count_list[i])
                create_cmt_images(image_list=image_list[left:right], comment=child_cmt)
                i += 1

        messages.success(request, "Reply created successfully.")

    return redirect("thread:feed")


@login_required
def get_thread(request, username, id):
    thread = get_object_or_404(Thread, pk=id)
    direct_comments = Comment.objects.filter(thread=thread, parent_comment=None)
    context = {"thread": thread, "direct_comments": direct_comments}
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/thread_page.html", context)
    return render(request, "thread/f_thread_page.html", context)


@login_required
def get_reply(request, username, id):
    comment = get_object_or_404(Comment, pk=id)
    context = {"comment": comment}
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/reply_page.html", context)
    return render(request, "thread/f_reply_page.html", context)
