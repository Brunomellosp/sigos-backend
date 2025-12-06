from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, "is_admin", lambda: False)()


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return user.is_authenticated and getattr(user, "is_admin", lambda: False)()
