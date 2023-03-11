from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == User.RoleChoices.ADMIN.value \
                    or request.user.is_superuser:
                return True
        return False


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.author
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == User.RoleChoices.MODERATOR.value:
                return True
        return False


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
