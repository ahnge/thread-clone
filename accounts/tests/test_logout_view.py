from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
