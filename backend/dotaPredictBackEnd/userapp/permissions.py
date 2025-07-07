from rest_framework.permissions import BasePermission

class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'analyst'