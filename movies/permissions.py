from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return request.user and request.user.is_superuser


class IsCritic(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_staff
            and request.user.is_superuser == False
        )


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_staff == False
            and request.user.is_superuser == False
        )
