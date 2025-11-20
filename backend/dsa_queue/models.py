
from django.db import models
from django.conf import settings  # still works because AUTH_USER_MODEL points to CustomUser

class Session(models.Model):
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    capacity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"


class Signup(models.Model):
    # Link to your custom user model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # this will resolve to accounts.CustomUser
        on_delete=models.CASCADE,
        related_name="signups"
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="signups"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("canceled", "Canceled")],
        default="active",
    )
    lc_level = models.CharField(
        max_length=10,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        null=True,
        blank=True,
    )
    discord_username = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.session.date}"
