from rest_framework import serializers
from .models import Session, Signup, EventTemplate, InterviewQueue
from rest_framework.exceptions import PermissionDenied

class SessionSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = "__all__"

    def get_permissions(self, obj):
        user = self.context["request"].user
        return {
            "can_view": True,
            "can_signup": user.is_authenticated and not obj.is_full(),
            "can_modify": user.is_authenticated and user.groups.filter(name="event_admin").exists(),
        }


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for Signup model.
    Ensures discord_username is auto-populated from the user if not provided.
    """

    class Meta:
        model = Signup
        fields = [
            "id",
            "user",
            "session",
            "created_at",
            "status",
            "lc_level",
            "discord_username",
        ]
        read_only_fields = ["user", "created_at", "status"]

    def create(self, validated_data):
        """
        Auto-fill user and discord_username from the request context.
        """
        user = self.context["request"].user
        validated_data["user"] = user
        if not validated_data.get("discord_username"):
            validated_data["discord_username"] = user.discord_username
        return super().create(validated_data)





class EventTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTemplate
        fields = [
            "id",
            "name",
            "day_of_week",
            "start_time",
            "end_time",
            "capacity",
            "start_date",
            "end_date",
            "created_by",
        ]
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        user = self.context["request"].user
        # Check permission before creating
        if not (user.is_superuser or user.groups.filter(name="event_admin").exists()):
            self.raise_permission_error()
        validated_data["created_by"] = user
        return super().create(validated_data)

    def raise_permission_error(self):
        """
        Helper method: raise a PermissionDenied error with a clear message.
        """
        raise PermissionDenied(detail="You do not have permission to create or modify event templates.")





class InterviewQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQueue
        fields = "__all__"
