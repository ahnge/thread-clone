from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError


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

    def clean_last_name(self):
        """Make last name to be required"""
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("This field is required.", code="no_last_name")

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
            return redirect("thread:feed")
        else:
            form = AuthenticationForm()
            return render(request, "registration/login.html", {"form": form})
    elif request.method == "GET":
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
