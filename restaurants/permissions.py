from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

class IsAdminOrAuthReadOnly(BasePermission):
    """
        Only Admins can perform All requests.
        Non-Admins can only perform GET requests.
    """
    def has_permission(self, request, view):
        # Allows anyone to perform GET requests
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        # Only Admin can perform any other action
        return IsAdminUser().has_permission(request, view)
        # Same as request.user.is_authenticated and request.user.is_staff