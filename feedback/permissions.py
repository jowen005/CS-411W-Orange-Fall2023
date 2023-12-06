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




# class FeedbackPermission(BasePermission):
#     def has_permission(self, request, view):
#         is_authenticated = request.user.is_authenticated 

#         if is_authenticated:
#             menu_item_id = request.data.get('menu_item_id', 0)
            
#             # No Menu Item specified
#             if menu_item_id == 0:
                
#                 # Patron can list, create, retrieve, update, and delete their own
#                 if request.user.user_type == 'patron':
#                     if view.action == 'list' or view.action == 'create':
#                         return True
#                     elif hasattr(view, 'get_object'):
#                         obj = view.get_object()
#                         return obj.patron == request.user
                    
#             # Menu Item Specified
#             elif menu_item_id > 0:

#                 # anyone can list all reviews for that item
#                 if view.action == 'list':
#                     return True
                
#         return False



# class FeedbackPermission(BasePermission):
#     def has_permission(self, request, view):
#         is_authenticated = request.user.is_authenticated 

#         if is_authenticated:
#             if request.user.user_type == 'patron':
#                 if view.action == 'list' or view.action == 'create':
#                     return True
#                 elif hasattr(view, 'get_object'):
#                     obj = view.get_object()
#                     return obj.patron == request.user
#             elif request.user.user_type == 'restaurant':
#                 rest_id = self.request.data.get('rest_id', 0)
#                 menu_item_id = self.request.data.get('menu_item_id', 0)
                
#                 if rest_id != 0 and menu_item_id != 0:
#                     rest = Restaurant.objects.get(pk=rest_id)
#                     menu_item = MenuItem.objects.get(pk=menu_item_id)

#                     if rest.owner == request.user and menu_item.restaurant == rest:
                        
#                         if view.action == 'list':
#                             return True

#         return False

