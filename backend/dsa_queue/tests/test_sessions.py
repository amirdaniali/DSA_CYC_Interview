from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from dsa_queue.models import Session

User = get_user_model()


class TestSessionAPI(APITestCase):
    """
    Tests for the Session API endpoints.
    Verifies that sessions can be listed publicly, but only event admins can create, update, or delete.
    """

    def setUp(self) -> None:
        """
        Create test users and a sample session.
        """
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.user = User.objects.create_user(
            username="alice", email="alice@example.com", password="password"
        )
        self.client = APIClient()
        self.session = Session.objects.create(
            date="2025-11-23",
            start_time="09:00:00",
            end_time="10:00:00",
            capacity=10,
            remaining_capacity=10,
            is_active=True,
        )

    def test_list_sessions_public(self) -> None:
        """
        Anonymous users should be able to list upcoming sessions.
        """
        url = reverse("session-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_session_requires_admin(self) -> None:
        """
        Only event admins can create sessions.
        """
        url = reverse("session-list")
        data = {"date": "2025-11-24", "start_time": "11:00:00", "end_time": "12:00:00", "capacity": 5}
        # Unauthenticated
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Authenticated non-admin
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_session_admin_only(self) -> None:
        """
        Only admins can update sessions.
        """
        url = reverse("session-detail", args=[self.session.id])
        data = {"capacity": 20}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_session_admin_only(self) -> None:
        """
        Only admins can delete sessions.
        """
        url = reverse("session-detail", args=[self.session.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
