# dsa_queue/tests/test_signups.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from dsa_queue.models import Session, Signup

User = get_user_model()

class TestSignupAPI(APITestCase):
    """
    Tests for Signup API endpoints.
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password",
            full_name="Alice Example",
            discord_username="alice#1234",
        )
        self.other_user = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="password",
            full_name="Bob Example",
            discord_username="bob#5678",
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
            full_name="Admin User",
            discord_username="admin#9999",
        )
        self.session = Session.objects.create(
            date="2025-11-23",
            start_time="09:00:00",
            end_time="10:00:00",
            capacity=2,
            remaining_capacity=2,
        )
        self.client = APIClient()

    def test_create_signup_authenticated_only(self) -> None:
        """
        Authenticated users can sign up for sessions.
        Anonymous users cannot.
        """
        url = reverse("signup-list")
        data = {"session": self.session.id, "lc_level": "easy"}

        # Anonymous
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        signup = Signup.objects.get(user=self.user, session=self.session)
        self.assertEqual(signup.discord_username, "alice#1234")

    def test_update_signup_owner_vs_other_vs_admin(self) -> None:
        """
        Only the owner or an admin can update a signup.
        """
        signup = Signup.objects.create(user=self.user, session=self.session, discord_username="alice#1234")
        url = reverse("signup-detail", args=[signup.id])
        data = {"lc_level": "medium"}

        # Other user
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, {"lc_level": "easy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_signup_owner_vs_other_vs_admin(self) -> None:
        """
        Only the owner or an admin can delete a signup.
        """
        signup = Signup.objects.create(user=self.user, session=self.session, discord_username="alice#1234")
        url = reverse("signup-detail", args=[signup.id])

        # Other user
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Admin
        signup = Signup.objects.create(user=self.user, session=self.session, discord_username="alice#1234")
        url = reverse("signup-detail", args=[signup.id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
