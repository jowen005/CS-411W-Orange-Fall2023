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
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS or request.user.user_type == 'admin':
                return True
            
        return False


class IsAuthenticatedAndRestaurantOwner(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated and is_restaurant:
            if view.action == 'list' or view.action == 'create':
                return True
            elif hasattr(view, 'get_object'):
                obj = view.get_object()
                return obj.owner == request.user
        
        return False
