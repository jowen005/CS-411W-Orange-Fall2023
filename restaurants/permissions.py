from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS)
from .models import Restaurant
from rest_framework.exceptions import PermissionDenied

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


class IsAuthRestAndIsOwner(BasePermission):
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


class IsAuthRestIsOwnerAndIsRest(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_restaurant = request.user.user_type == 'restaurant'

        if is_authenticated and is_restaurant:
            # Grab all restaurants that this user owns
            owned_rest_ids = list(Restaurant.objects.filter(owner=request.user).values_list('id',flat=True))
            requested_id = view.kwargs.get('restaurant_id')

            # If the requested_id is owned by the user
            if requested_id in owned_rest_ids:
                restaurant = Restaurant.objects.get(pk=requested_id)
                if view.action == 'list' or view.action == 'create':
                    return True
                elif hasattr(view, 'get_object'):
                    obj = view.get_object()
                    return obj.restaurant == restaurant
            
            raise PermissionDenied("This restaurant does not have access to this restaurant's menu items")
        
        else:
            raise PermissionDenied("This user is not of type 'restaurant' or is not authenticated")
        
        
