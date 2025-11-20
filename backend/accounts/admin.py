from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from dsa_queue.models import EventTemplate, Session, Signup


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser.
    Displays email, username, full_name, discord_username.
    Adds an action to promote users to Event Admins.
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "full_name", "discord_username", "is_staff", "is_active"]

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("full_name", "discord_username")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "full_name", "discord_username", "password1", "password2", "is_active", "is_staff"),
        }),
    )

    actions = ["make_event_admin"]

    def make_event_admin(self, request, queryset) -> None:
        """
        Promote selected users to Event Admins by adding them to the 'event_admin' group
        and assigning the correct model permissions.
        :param request: HttpRequest object
        :param queryset: Queryset of selected CustomUser objects
        :return: None
        """
        event_admin_group, created = Group.objects.get_or_create(name="event_admin")

        if created:
            for model in [EventTemplate, Session, Signup]:
                ct = ContentType.objects.get_for_model(model)
                perms = Permission.objects.filter(content_type=ct)
                event_admin_group.permissions.add(*perms)

        for user in queryset:
            user.groups.add(event_admin_group)

        self.message_user(request, "Selected users promoted to Event Admins.")

    make_event_admin.short_description = "Create new Event Admin with proper permissions"


admin.site.register(CustomUser, CustomUserAdmin)
