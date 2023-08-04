from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.views import CustomUserCreationForm


class RegisterViewTestCase(TestCase):
    def test_register_view_GET(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_register_view_POST_valid_data(self):
        data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        response = self.client.post(reverse("accounts:register"), data, follow=True)
        self.assertRedirects(response, reverse("thread:feed"))
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_view_POST_invalid_data(self):
        data = {
            "username": "testuser",
            "first_name": "",  # Missing first_name
            "last_name": "Doe",
            "email": "",  # Missing email
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        response = self.client.post(reverse("accounts:register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "first_name", "This field is required.")
        self.assertFormError(response, "form", "email", "Email field is required.")
