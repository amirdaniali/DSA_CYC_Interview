from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name="event_admin").exists()



class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class that allows only the owner of an object
    or an event admin/superuser to modify/delete it.
    Safe methods are always allowed.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user == request.user:
            return True
        return request.user.is_superuser or request.user.groups.filter(name="event_admin").exists()




class IsEventAdmin(permissions.BasePermission):
    """
    Strict: requires authenticated AND superuser or member of 'event_admin' group.
    Applies to ALL methods (including GET/HEAD/OPTIONS).
    """

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or user.groups.filter(name="event_admin").exists()
