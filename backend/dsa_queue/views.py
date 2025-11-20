from rest_framework import viewsets, permissions
from django.utils.timezone import now
from .models import Session, Signup, EventTemplate, InterviewQueue
from .serializers import SignupSerializer, SessionSerializer, EventTemplateSerializer, InterviewQueueSerializer
from .permissions import IsOwnerOrAdmin, IsEventAdmin


from rest_framework.permissions import IsAuthenticated
from dsa_queue.models import Signup
from dsa_queue.serializers import SignupSerializer
from dsa_queue.permissions import IsOwnerOrAdmin

class IsEventAdmin(permissions.BasePermission):
    """
    Custom permission: only users in 'event_admin' group or superusers can modify.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return (
            user
            and user.is_authenticated
            and (user.is_superuser or user.groups.filter(name="event_admin").exists())
        )



class SessionViewSet(viewsets.ModelViewSet):
    """
    Anonymous: read-only
    Authenticated: read-only
    Admins: full CRUD
    """
    serializer_class = SessionSerializer
    permission_classes = [IsEventAdmin]

    def get_queryset(self):
        # Only show upcoming sessions
        return Session.objects.filter(date__gte=now().date(), is_active=True)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()




class SignupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing signups.
    - Authenticated users can create their own signups.
    - Owners or admins can update/delete.
    - Anyone can list signups.
    """
    queryset = Signup.objects.all()
    serializer_class = SignupSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return []  # list/retrieve are public



class EventTemplateViewSet(viewsets.ModelViewSet):
    queryset = EventTemplate.objects.all()
    serializer_class = EventTemplateSerializer

    # Apply strict admin-only for ALL actions
    permission_classes = [IsEventAdmin]

    # Optionally, harden by returning an instance each time (not required, but removes ambiguity)
    def get_permissions(self):
        return [IsEventAdmin()]






class InterviewQueueViewSet(viewsets.ModelViewSet):
    """
    Queue management restricted to event admins.
    """
    queryset = InterviewQueue.objects.all()
    serializer_class = InterviewQueueSerializer
    permission_classes = [IsEventAdmin]
