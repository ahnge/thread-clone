from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )

    def test_login_view_GET(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertIsInstance(response.context["form"], AuthenticationForm)

    def test_login_view_POST_valid_credentials(self):
        data = {
            "username": "testuser",
            "password": "testpassword123",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertRedirects(response, reverse("thread:feed"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_POST_invalid_credentials(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword",  # Incorrect password
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["error"], "Please enter a correct username and password."
        )

    def test_login_view_POST_nonexistent_user(self):
        data = {
            "username": "nonexistentuser",  # Nonexistent username
            "password": "testpassword123",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["error"], "Please enter a correct username and password."
        )
