from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAuthPatron(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        is_patron = request.user.user_type == 'patron'

        if is_authenticated and is_patron:
            return True
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated patron!")


class IsAuthPatronAndIsUser(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated 
        is_patron = request.user.user_type == 'patron'

        if is_authenticated and is_patron:
            if view.action == 'list' or view.action == 'create':
                return True
            elif hasattr(view, 'get_object'):
                obj = view.get_object()
                return obj.user == request.user
        
        return False
    
class IsAuthPatronIsUserNoUpdate(IsAuthPatronAndIsUser):
    def has_permission(self, request, view):
        if view.action == 'update':
            return False
        is_authenticated = request.user.is_authenticated 
        is_patron = request.user.user_type == 'patron'

        if is_authenticated and is_patron:
            if view.action == 'list' or view.action == 'create':
                return True
            elif hasattr(view, 'get_object'):
                obj = view.get_object()
                return obj.patron == request.user
        
        return False