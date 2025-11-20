# backend/queue/views.py
from rest_framework import viewsets, permissions, filters
from .models import Session, Signup
from .serializers import SessionSerializer, SignupSerializer
from django.db import models


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return request.user.is_staff

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all().annotate(signup_count=models.Count("signups", filter=models.Q(signups__status="active")))
    serializer_class = SessionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["date", "is_active"]

class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Signup.objects.select_related("user", "session").filter(status="active")
        session_id = self.request.query_params.get("session_id")
        if session_id:
            qs = qs.filter(session_id=session_id).order_by("created_at")
        else:
            qs = qs.order_by("-created_at")
        # Users can see everyone; restrict write ops to owner
        return qs

    def perform_destroy(self, instance):
        # soft cancel to preserve ordering gaps explicitly
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Not allowed")
        instance.status = "canceled"
        instance.save()
