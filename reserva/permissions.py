from rest_framework import permissions
from accounts.models import User


class IsBooker(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user == User.BOOKER or request.user.is_superuser:
            return True
        return False