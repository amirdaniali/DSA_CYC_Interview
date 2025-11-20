from django.contrib import admin
from .models import EventTemplate, Session, Signup, InterviewQueue

@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "day_of_week", "start_time", "end_time", "capacity", "start_date", "end_date")
    actions = ["generate_sessions_action"]

    def generate_sessions_action(self, request, queryset):
        for template in queryset:
            template.generate_sessions()
    generate_sessions_action.short_description = "Generate sessions from template"


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "end_time", "capacity", "remaining_capacity", "is_active")


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "created_at", "status")


@admin.register(InterviewQueue)
class InterviewQueueAdmin(admin.ModelAdmin):
    list_display = ("signup", "position")
