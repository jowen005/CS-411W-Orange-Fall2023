from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS)
from restaurants.models import Restaurant
from rest_framework.exceptions import PermissionDenied


class IsAuthAndAdminAndList(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        
        if is_authenticated and is_admin:
            if view.action == 'list':
                return True
        
        return False
    

class IsAuthAndNotPatronAndList(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated and (is_admin or is_restaurant):
            if view.action == 'list':
                return True
        
        return False
    

class LocalMenuItemPermission(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated:
            if is_admin and view.action =='list':
                return True
            
            if is_restaurant and view.action =='list':
                owned_rest_ids = list(Restaurant.objects.filter(owner=request.user).values_list('id',flat=True))
                requested_id = view.kwargs.get('restaurant_id')
                
                if requested_id in owned_rest_ids:
                    return True
                raise PermissionDenied("This user does not have access to the specified restaurant's menu item analytics.")

            raise PermissionDenied(f"The request is not a List action or the user is not a restaurant/admin.")

        raise PermissionDenied("This user is not authenticated.")
    
