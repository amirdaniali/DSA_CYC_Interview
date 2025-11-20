# backend/queue/serializers.py
from rest_framework import serializers
from .models import Session, Signup

class SessionSerializer(serializers.ModelSerializer):
    signup_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Session
        fields = ["id", "date", "start_time", "end_time", "capacity", "is_active", "signup_count"]

class SignupSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Signup
        fields = ["id", "user", "user_name", "session", "created_at", "status", "lc_level"]
        read_only_fields = ["user", "created_at", "status"]

    def create(self, validated):
        request = self.context["request"]
        validated["user"] = request.user
        # enforce capacity
        session = validated["session"]
        active_count = session.signups.filter(status="active").count()
        if not session.is_active:
            raise serializers.ValidationError("This session is closed.")
        if active_count >= session.capacity:
            raise serializers.ValidationError("Session is at capacity.")
        return super().create(validated)
