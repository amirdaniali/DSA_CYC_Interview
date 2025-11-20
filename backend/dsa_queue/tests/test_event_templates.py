# dsa_queue/tests/test_event_templates.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from dsa_queue.models import EventTemplate

User = get_user_model()


class TestEventTemplateAPI(APITestCase):
    """
    Tests for EventTemplate API endpoints.
    Only event admins or superusers can access.
    """

    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.user = User.objects.create_user(
            username="alice", email="alice@example.com", password="password"
        )
        self.client = APIClient()

    # ---- LIST TESTS ----
    def test_list_templates_non_admin_forbidden(self) -> None:
        """Non-admin users should NOT be able to list templates."""
        url = reverse("template-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_templates_admin_allowed(self) -> None:
        """Admin users should be able to list templates."""
        url = reverse("template-list")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_templates_anonymous_forbidden(self) -> None:
        """Anonymous users should NOT be able to list templates."""
        url = reverse("template-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_templates_admin_with_existing_template(self) -> None:
        """Admin should see templates if they exist."""
        EventTemplate.objects.create(
            name="Test Template",
            day_of_week=1,
            start_time="14:00:00",
            end_time="15:00:00",
            capacity=5,
            start_date="2025-11-25",
            end_date="2026-02-25",
            created_by=self.admin,
        )
        url = reverse("template-list")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # ---- CREATE TESTS ----
    def test_create_template_non_admin_forbidden(self) -> None:
        """Non-admin users should NOT be able to create templates."""
        url = reverse("template-list")
        data = {
            "name": "Tuesday Afternoon Interviews",
            "day_of_week": 1,
            "start_time": "14:00:00",
            "end_time": "15:00:00",
            "capacity": 5,
            "start_date": "2025-11-25",
            "end_date": "2026-02-25",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_template_admin_allowed(self) -> None:
        """Admin users should be able to create templates."""
        url = reverse("template-list")
        data = {
            "name": "Tuesday Afternoon Interviews",
            "day_of_week": 1,
            "start_time": "14:00:00",
            "end_time": "15:00:00",
            "capacity": 5,
            "start_date": "2025-11-25",
            "end_date": "2026-02-25",
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventTemplate.objects.count(), 1)

    def test_create_template_anonymous_forbidden(self) -> None:
        """Anonymous users should NOT be able to create templates."""
        url = reverse("template-list")
        data = {
            "name": "Anonymous Template",
            "day_of_week": 2,
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "capacity": 3,
            "start_date": "2025-11-25",
            "end_date": "2026-02-25",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_template_admin_invalid_data(self) -> None:
        """Admin should get 400 if data is invalid."""
        url = reverse("template-list")
        data = {
            "name": "",  # invalid
            "day_of_week": 1,
            "start_time": "14:00:00",
            "end_time": "15:00:00",
            "capacity": -1,  # invalid
            "start_date": "2025-11-25",
            "end_date": "2026-02-25",
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
