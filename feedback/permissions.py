from rest_framework.permissions import BasePermission
from restaurants.models import Restaurant, MenuItem

from rest_framework.exceptions import PermissionDenied

class FeedbackPermission(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated 

        if is_authenticated:
            
            # Anyone can list menu item reviews (lists all reviews for a specific menu item)
            if view.action == 'list':
                raise PermissionDenied(f"This action is not allowed ({view.action})!")        

            # Patrons can perform other actions on their data
            if request.user.user_type == 'patron':
                if view.action == 'create':
                    return True
                elif hasattr(view, 'get_object'):
                    obj = view.get_object()
                    return obj.patron == request.user
                
            raise PermissionDenied(f'This user is not a valid authenticated patron!')
                
        raise PermissionDenied(f'This user is not authenticated!')
    

class IsAuth(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated

        if is_authenticated:
            return True

        raise PermissionDenied(f'This user is not authenticated!')
        
    

class AdminReadNonAdminWrite(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        user_type = request.user.user_type

        if is_authenticated:
            if user_type == 'admin' and view.action == 'list':
                return True
            elif user_type != 'admin' and view.action == 'create':
                return True
            
        return False

