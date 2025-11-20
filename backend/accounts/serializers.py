from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "discord_username"]





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token["username"] = user.username
        # token["email"] = user.email
        # token["discord_username"] = getattr(user, "discord_username", "")
        # token["full_name"] = getattr(user, "full_name", "")
        # token["id"] = getattr(user, "id", "")
        # token["permissions"] = list(user.get_all_permissions())
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["discord_username"] = getattr(self.user, "discord_username", "")
        data["full_name"] = getattr(self.user, "full_name", "")
        data["id"] = getattr(self.user, "id", "")
        # data["permissions"] = list(self.user.get_all_permissions())
        data["role"] =  "admin" if len(self.user.get_all_permissions()) > 0 else "user"
        # data["roles"] = [g.name for g in self.user.groups.all()]
        return data




class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "full_name", "discord_username"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
            discord_username=validated_data.get("discord_username", ""),
        )
        return user
