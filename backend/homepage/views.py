# backend/queue/views.py
from rest_framework import viewsets, permissions, filters
from .models import Session, Signup

from django.db import models
from .serializers import SignupSerializer, SessionSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return request.user.is_staff

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class SignupViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # Automatically set the creating user
        serializer.save(user=self.request.user)
