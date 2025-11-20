# accounts/tests/test_users.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password",
            full_name="Alice Example",
            discord_username="alice#1234",
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
            full_name="Admin User",
            discord_username="admin#9999",
        )
        self.client = APIClient()

    def test_users_list_anonymous_denied(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_list_normal_user_only_self(self):
        url = reverse("user-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "alice")

    def test_users_list_admin_all_users(self):
        url = reverse("user-list")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [u["username"] for u in response.data]
        self.assertIn("alice", usernames)
        self.assertIn("admin", usernames)

    def test_users_detail_normal_user_self_only(self):
        url = reverse("user-detail", args=[self.user.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to access another user
        url = reverse("user-detail", args=[self.admin.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_users_detail_admin_can_access_any(self):
        url = reverse("user-detail", args=[self.user.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "alice")
