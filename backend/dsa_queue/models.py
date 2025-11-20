from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class EventTemplate(models.Model):
    """
    Defines recurring rules for sessions (e.g., every Tuesday at 2 PM for 3 months).
    """

    name: models.CharField = models.CharField(max_length=100)
    day_of_week: models.IntegerField = models.IntegerField(
        choices=[(0,"Monday"),(1,"Tuesday"),(2,"Wednesday"),
                 (3,"Thursday"),(4,"Friday"),(5,"Saturday"),(6,"Sunday")]
    )
    start_time: models.TimeField = models.TimeField()
    end_time: models.TimeField = models.TimeField()
    capacity: models.PositiveIntegerField = models.PositiveIntegerField(default=1)
    start_date: models.DateField = models.DateField()
    end_date: models.DateField = models.DateField()
    created_by: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_event_templates"
    )

    def __str__(self) -> str:
        """
        Returns the string representation of the template.
        :return: Template name and day of week
        """
        return f"{self.name} ({self.get_day_of_week_display()})"

    def generate_sessions(self) -> None:
        """
        Auto-create Session objects between start_date and end_date
        for the given day_of_week.
        :return: None
        """
        import datetime
        current = self.start_date
        while current <= self.end_date:
            if current.weekday() == self.day_of_week:
                Session.objects.get_or_create(
                    template=self,
                    date=current,
                    defaults={
                        "start_time": self.start_time,
                        "end_time": self.end_time,
                        "capacity": self.capacity,
                        "remaining_capacity": self.capacity,
                    },
                )
            current += datetime.timedelta(days=1)


class Session(models.Model):
    """
    Concrete instance of an event (e.g., Tuesday Nov 25, 2025, 2 PM).
    """

    template = models.ForeignKey(EventTemplate, on_delete=models.CASCADE, related_name="sessions", null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    capacity = models.PositiveIntegerField(default=1)
    remaining_capacity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def is_full(self) -> bool:
        """
        Check if the session is full.
        :return: True if remaining_capacity <= 0, else False
        """
        return self.remaining_capacity <= 0

    def decrement_capacity(self) -> None:
        """
        Decrease remaining_capacity by 1 if greater than 0.
        :return: None
        """
        if self.remaining_capacity > 0:
            self.remaining_capacity -= 1
            self.save()

    def increment_capacity(self) -> None:
        """
        Increase remaining_capacity by 1 if less than capacity.
        :return: None
        """
        if self.remaining_capacity < self.capacity:
            self.remaining_capacity += 1
            self.save()

    def __str__(self) -> str:
        """
        Returns the string representation of the session.
        :return: Date and time range
        """
        return f"{self.date} {self.start_time}-{self.end_time}"


class Signup(models.Model):
    """
    Tracks user sign-ups for sessions and preserves queue order.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="signups")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="signups")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("active", "Active"), ("canceled", "Canceled")], default="active")
    lc_level = models.CharField(max_length=10, choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], null=True, blank=True)
    discord_username = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ("user", "session")
        ordering = ["created_at"]

    def __str__(self) -> str:
        """
        Returns the string representation of the signup.
        :return: Username and session date
        """
        return f"{self.user.username} → {self.session.date}"


class InterviewQueue(models.Model):
    """
    Optional abstraction if you want a global queue across sessions.
    Each signup gets a queue entry with a position.
    """

    signup = models.OneToOneField(Signup, on_delete=models.CASCADE, related_name="queue_entry")
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ["position"]

    def __str__(self) -> str:
        """
        Returns the string representation of the queue entry.
        :return: Queue position and username
        """
        return f"Queue #{self.position}: {self.signup.user.username}"