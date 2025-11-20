# backend/queue/serializers.py
from rest_framework import serializers
from .models import Session, Signup

class SessionSerializer(serializers.ModelSerializer):
    signup_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Session
        fields = ["id", "date", "start_time", "end_time", "capacity", "is_active", "signup_count"]



class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ["id", "session", "lc_level", "discord_username", "status", "created_at"]
        extra_kwargs = {
            "session": {"required": True},
        }

    def validate(self, attrs):
        # Reject unknown fields explicitly
        for key in self.initial_data.keys():
            if key not in self.fields:
                raise serializers.ValidationError({key: "This field is not allowed."})
        return attrs
