from django.test import TestCase
from django.contrib.auth import get_user_model
from dsa_queue.models import Session, Signup, InterviewQueue

User = get_user_model()


class TestInterviewQueue(TestCase):
    """
    Tests for InterviewQueue model to ensure ordering and linkage to signups.
    """

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username="alice", email="alice@example.com", password="password")
        self.user2 = User.objects.create_user(username="bob", email="bob@example.com", password="password")
        self.session = Session.objects.create(date="2025-11-23", start_time="09:00:00", end_time="10:00:00", capacity=2, remaining_capacity=2)
        self.signup1 = Signup.objects.create(user=self.user1, session=self.session)
        self.signup2 = Signup.objects.create(user=self.user2, session=self.session)

    def test_queue_ordering(self) -> None:
        """
        Queue entries should respect position ordering.
        """
        q1 = InterviewQueue.objects.create(signup=self.signup1, position=1)
        q2 = InterviewQueue.objects.create(signup=self.signup2, position=2)
        queues = InterviewQueue.objects.all()
        self.assertEqual(list(queues), [q1, q2])

    def test_queue_str(self) -> None:
        """
        __str__ should return readable representation.
        """
        q1 = InterviewQueue.objects.create(signup=self.signup1, position=1)
        self.assertIn("Queue #1", str(q1))
        self.assertIn(self.signup1.user.username, str(q1))
