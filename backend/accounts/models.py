from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Removes first_name and last_name, and adds mandatory fields:
    - email: unique and required
    - full_name: required full name
    - discord_username: required Discord handle
    """

    # Remove first_name and last_name
    first_name = None
    last_name = None

    email: models.EmailField = models.EmailField(unique=True, blank=False, null=False)
    full_name: models.CharField = models.CharField(max_length=150, blank=False, null=False)
    discord_username: models.CharField = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        """
        Returns the string representation of the user.
        :return: User's email address
        """
        return self.email
