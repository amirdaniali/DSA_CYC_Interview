
from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Admins can access all users.
    Normal users can only access their own record.
    Guests cannot access anything.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user
