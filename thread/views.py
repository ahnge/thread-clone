from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Thread, Comment, Like, LikeComment, Repost, RepostComment
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
    paginator = Paginator(threads, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"threads": page_obj}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(request, "thread/partials/_more_feed.html", context)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/partials/_feed.html", context)
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
def get_thread_reply_form(request, id):
    if request.META.get("HTTP_HX_REQUEST"):
        thread = get_object_or_404(Thread, pk=id)
        context = {"thread": thread}
        return render(request, "partials/htmx/_thread_reply_form.html", context)
    return redirect("thread:feed")


@login_required
def get_comment_reply_form(request, id):
    if request.META.get("HTTP_HX_REQUEST"):
        comment = get_object_or_404(Comment, pk=id)
        context = {"comment": comment}
        return render(request, "partials/htmx/_comment_reply_form.html", context)
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

        if parent_comment:
            return redirect(
                "thread:get_reply",
                username=parent_comment.user.username,
                id=int(comment_id),
            )
        else:
            return redirect(
                "thread:get_thread", username=thread.user.username, id=int(thread_id)
            )

    return redirect("thread:feed")


@login_required
def get_thread(request, username, id):
    thread = get_object_or_404(Thread, pk=id)
    direct_comments = Comment.objects.filter(thread=thread, parent_comment=None)

    paginator = Paginator(direct_comments, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"thread": thread, "direct_comments": page_obj}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(
            request,
            "thread/htmx/partials/_more_comment_section_for_thread_page.html",
            context,
        )
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/thread_page.html", context)
    return render(request, "thread/f_thread_page.html", context)


@login_required
def get_reply(request, username, id):
    comment = get_object_or_404(Comment, pk=id)
    sub_comments = Comment.objects.filter(parent_comment=comment, thread=comment.thread)

    paginator = Paginator(sub_comments, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"comment": comment, "sub_comments": page_obj}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(
            request,
            "thread/htmx/partials/_more_comment_section_for_reply_page.html",
            context,
        )
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/reply_page.html", context)
    return render(request, "thread/f_reply_page.html", context)


@login_required
def like_thread_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        thread = get_object_or_404(Thread, pk=id)
        try:
            like_obj = Like.objects.get(thread=thread, user=request.user)
            like_obj.delete()
        except Like.DoesNotExist:
            Like.objects.create(thread=thread, user=request.user)
        return HttpResponse("Success!")
    return redirect("thread:feed")


@login_required
def like_comment_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        comment = get_object_or_404(Comment, pk=id)
        try:
            like_cmt_obj = LikeComment.objects.get(comment=comment, user=request.user)
            like_cmt_obj.delete()
        except LikeComment.DoesNotExist:
            LikeComment.objects.create(comment=comment, user=request.user)
        return HttpResponse("Success!")
    return redirect("thread:feed")


@login_required
def search(request):
    users = User.objects.all().order_by("-date_joined")
    paginator = Paginator(users, 10)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)

    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(
            request,
            "thread/htmx/partials/_more_search.html",
            {"page_obj": page_obj},
        )

    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/search.html", {"page_obj": page_obj})
    return render(request, "thread/f_search.html", {"page_obj": page_obj})


@login_required
def search_query(request):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        q = request.POST.get("search")
        users = User.objects.filter(username__icontains=q).order_by("-date_joined")
        paginator = Paginator(users, 10)
        page_number = request.GET.get("page") or 1

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_number = 1
        except EmptyPage:
            page_number = 1

        page_obj = paginator.page(page_number)

        return render(
            request,
            "thread/htmx/partials/_search_query.html",
            {"page_obj": page_obj},
        )
    else:
        return redirect("thread:search")


@login_required
def repost_thread_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        thread = get_object_or_404(Thread, pk=id)
        try:
            repost_obj = Repost.objects.get(thread=thread, user=request.user)
            repost_obj.delete()
            messages.success(request, "Thread repost deleted.")
        except Repost.DoesNotExist:
            Repost.objects.create(thread=thread, user=request.user)
            messages.success(request, "Thread reposted.")
        return render(request, "htmx/partials/_notification_messages.html")
    return redirect("thread:feed")


@login_required
def repost_comment_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        comment = get_object_or_404(Comment, pk=id)
        try:
            repost_cmt_obj = RepostComment.objects.get(
                comment=comment, user=request.user
            )
            repost_cmt_obj.delete()
            messages.success(request, "Comment repost deleted.")
        except RepostComment.DoesNotExist:
            RepostComment.objects.create(comment=comment, user=request.user)
            messages.success(request, "Comment reposted.")
        return render(request, "htmx/partials/_notification_messages.html")
    return redirect("thread:feed")
