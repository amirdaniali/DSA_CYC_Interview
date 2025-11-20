# homepage/models.py
from django.db import models

class Session(models.Model):
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    capacity = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"


class Signup(models.Model):
    # Instead of linking to auth_user, just store basic info
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True) 
    discord_username = models.CharField(max_length=100, blank=True, null=True)  
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="signups")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("canceled", "Canceled")],
        default="active",
    )
    lc_level = models.CharField(
        max_length=10,
        choices=[("easy", "Easy"), ("medium", "Medium")],
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.name} ({self.session.date})"
