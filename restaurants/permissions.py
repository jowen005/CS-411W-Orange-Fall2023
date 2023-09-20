from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS)

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


class IsAuthenticatedAndRestaurantOwner(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated and is_restaurant:
            if view.action == 'list' or view.action == 'create':
                return True
            elif hasattr(view, 'get_object'):
                obj = view.get_object()
                # is_owner = obj.owner == request.user
                return True
        
        return False
