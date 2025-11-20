from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory
from dsa_queue.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from dsa_queue.models import Session, Signup

User = get_user_model()


class TestPermissions(TestCase):
    """
    Unit tests for custom permission classes.
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="alice", email="alice@example.com", password="password")
        self.other_user = User.objects.create_user(username="bob", email="bob@example.com", password="password")
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="password")
        event_admin_group, _ = Group.objects.get_or_create(name="event_admin")
        self.admin.groups.add(event_admin_group)

        self.session = Session.objects.create(
            date="2025-11-23", start_time="09:00:00", end_time="10:00:00", capacity=2, remaining_capacity=2
        )
        self.signup = Signup.objects.create(user=self.user, session=self.session)

        self.factory = APIRequestFactory()

    def test_is_owner_or_admin(self) -> None:
        """
        Owner or event_admin should have permission, others should not.
        """
        perm = IsOwnerOrAdmin()

        # Owner with safe method
        request = self.factory.get("/")
        request.user = self.user
        self.assertTrue(perm.has_object_permission(request, None, self.signup))

        # Other user with unsafe method
        request = self.factory.patch("/")
        request.user = self.other_user
        self.assertFalse(perm.has_object_permission(request, None, self.signup))

        # Admin with unsafe method
        request = self.factory.patch("/")
        request.user = self.admin
        self.assertTrue(perm.has_object_permission(request, None, self.signup))

    def test_is_admin_or_read_only(self) -> None:
        """
        Admins can modify, others can only read.
        """
        perm = IsAdminOrReadOnly()

        # Safe method always allowed
        request = self.factory.get("/")
        request.user = self.user
        self.assertTrue(perm.has_permission(request, None))

        # Non-admin POST denied
        request = self.factory.post("/")
        request.user = self.user
        self.assertFalse(perm.has_permission(request, None))

        # Admin POST allowed
        request = self.factory.post("/")
        request.user = self.admin
        self.assertTrue(perm.has_permission(request, None))
