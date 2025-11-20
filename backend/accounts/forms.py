from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new CustomUser instances.
    Includes mandatory fields: username, email, full_name, discord_username.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "full_name", "discord_username")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating CustomUser instances.
    Includes mandatory fields: username, email, full_name, discord_username.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email", "full_name", "discord_username")
