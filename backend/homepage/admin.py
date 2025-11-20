# homepage/admin.py
from django.contrib import admin
from .models import Session, Signup

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "end_time", "capacity", "is_active")
    list_filter = ("date", "is_active")
    search_fields = ("date",)


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ("user", "discord_username", "session", "created_at", "status", "lc_level")
    list_filter = ("status", "lc_level", "session")
    search_fields = ("user__username", "user__email", "discord_username", "session__date")
