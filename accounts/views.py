from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse
from itertools import chain


from thread.models import Comment, Thread, RepostComment, Follow
from .utils import check_following


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_first_name(self):
        """Make first name to be required"""
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("This field is required.", code="no_first_name")
        return first_name

    def clean_last_name(self):
        """Make last name to be required"""
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("This field is required.", code="no_last_name")
        return last_name

    def clean_email(self):
        """Reject emails that already exists and reject if email is not specified."""
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email field is required.", code="no_email")
        elif email and self._meta.model.objects.filter(email__iexact=email).exists():
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration success.")
            return redirect("thread:feed")
        return render(request, "registration/register.html", {"form": form})
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logined.")
            return redirect("thread:feed")
        else:
            form = AuthenticationForm(request.POST)
            return render(
                request,
                "registration/login.html",
                {
                    "form": form,
                    "error": "Please enter a correct username and password.",
                },
            )
    elif request.method == "GET":
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    threads = Thread.objects.filter(user=user)

    paginator = Paginator(threads, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)

    # check followed or not
    already_followed = check_following(request.user, user)

    context = {"threads": page_obj, "u": user, "already_followed": already_followed}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(request, "accounts/htmx/profile_threads.html", context)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "accounts/htmx/profile.html", context)
    return render(request, "accounts/f_profile.html", context)


@login_required
def profile_threads(request, username):
    user = get_object_or_404(User, username=username)
    threads = Thread.objects.filter(user=user)

    paginator = Paginator(threads, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(
            request,
            "accounts/htmx/profile_threads.html",
            {"threads": page_obj, "u": user},
        )
    return redirect("accounts:profile", user)


@login_required
def profile_replies(request, username):
    user = get_object_or_404(User, username=username)
    replies = Comment.objects.filter(user=user).exclude(
        Q(parent_comment__isnull=False, parent_comment__user=user)
        | Q(parent_comment__isnull=True, thread__user=user)
    )

    paginator = Paginator(replies, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(
            request,
            "accounts/htmx/profile_replies.html",
            {"u": user, "replies": page_obj},
        )
    return redirect("accounts:profile", user)


@login_required
def profile_reposts(request, username):
    user = get_object_or_404(User, username=username)
    reposted_threads = user.reposted_threads.all()
    reposted_comments = user.reposted_comments.all()

    # Combine the two querysets into a single queryset
    merged_queryset = list(chain(reposted_threads, reposted_comments))

    # Sort the merged queryset based on created_at
    sorted_queryset = sorted(
        merged_queryset, key=lambda item: item.created_at, reverse=True
    )

    paginator = Paginator(sorted_queryset, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)

    if request.META.get("HTTP_HX_REQUEST"):
        return render(
            request,
            "accounts/htmx/profile_reposts.html",
            {"u": user, "reposts": page_obj},
        )
    return redirect("accounts:profile", user)


@login_required
def follow_toggle(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        try:
            follow_obj = Follow.objects.get(follower=request.user, followed=user)
            follow_obj.delete()
        except Follow.DoesNotExist:
            Follow.objects.create(follower=request.user, followed=user)
        follower_count = Follow.objects.filter(followed=user).count()
        if follower_count == 1:
            return HttpResponse(f"{follower_count} follower")
        else:
            return HttpResponse(f"{follower_count} followers")
    return redirect("accounts:profile", user)


@login_required
def profile_followers(request, username):
    user = get_object_or_404(User, username=username)
    # get the followers of this user
    follow_objs = user.followers.all()
    followers = [f.follower for f in follow_objs]

    # Annotate each user with a flag indicating whether the authenticated user is following them
    for f in followers:
        f.is_followed_by_authenticated_user = Follow.objects.filter(
            follower=request.user, followed=f
        ).exists()

    paginator = Paginator(followers, 15)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)

    if request.META.get("HTTP_HX_REQUEST"):
        return render(
            request,
            "accounts/htmx/partials/_profile_followers.html",
            {"followers": page_obj},
        )
    return redirect("accounts:profile", user)


@login_required
def profile_following(request, username):
    user = get_object_or_404(User, username=username)
    # get the followers of this user
    follow_objs = user.following.all()
    following = [f.followed for f in follow_objs]

    # Annotate each user with a flag indicating whether the authenticated user is following them
    for f in following:
        f.is_followed_by_authenticated_user = Follow.objects.filter(
            follower=request.user, followed=f
        ).exists()

    paginator = Paginator(following, 15)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)

    if request.META.get("HTTP_HX_REQUEST"):
        return render(
            request,
            "accounts/htmx/partials/_profile_following.html",
            {"following": page_obj},
        )
    return redirect("accounts:profile", user)


@login_required
def profile_edit(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        bio = request.POST.get("bio")
        link = request.POST.get("link")
        profile_image = request.FILES.get("profile_image")
        print(request.FILES)
        print(profile_image)

        # Update the User modal
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update the Myuser modal
        if bio:
            user.myuser.bio = bio
        if link:
            user.myuser.link = link
        if profile_image:
            user.myuser.profile_picture = profile_image
        user.myuser.save()

    return redirect("accounts:profile", user)
