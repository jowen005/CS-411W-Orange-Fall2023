from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS)
from restaurants.models import Restaurant, MenuItem
from rest_framework.exceptions import PermissionDenied


VALID_FILTER_TYPES = ['calories', 'restrictiontag', 'allergytag', 
                      'ingredienttag', 'tastetag', 'cookstyletag']


class IsNonPatronRetrieveAndValidFilter(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated 
        is_not_patron = request.user.user_type != 'patron'

        if view.action != 'retrieve':
            raise PermissionDenied(f"This action is not allowed ({view.action})! This API is retrieve only.")        

        filter_type = view.kwargs.get('filter_type')
        if filter_type not in VALID_FILTER_TYPES:
            raise PermissionDenied(f"{filter_type.title()} is not a valid filter!")
        
        if is_authenticated and is_not_patron:
            return True
        
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated admin or restaurant user!")
    

class LocalMenuItemTrendPermission(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        is_restaurant = request.user.user_type == 'restaurant'
        
        if view.action != 'retrieve':
            raise PermissionDenied(f"This action is not allowed ({view.action})! This API is retrieve only.")

        if is_authenticated:
            if is_admin:
                rest_id = view.kwargs.get('restaurant_id')
                item_id = int(view.kwargs.get('pk'))

                try:
                    item = MenuItem.objects.get(pk=item_id)
                except MenuItem.DoesNotExist:
                    raise PermissionDenied(f"This Menu Item ID ({item_id}) is not valid!")
                
                if item.restaurant.id == rest_id:
                    return True
                raise PermissionDenied(f"The specified menu item ({item_id}) does not belong " +
                                        f"to the specified restaurant ({rest_id})!")
            
            if is_restaurant:
                owned_rest_ids = list(Restaurant.objects.filter(owner=request.user).values_list('id',flat=True))
                rest_id = view.kwargs.get('restaurant_id')
                
                if rest_id in owned_rest_ids:
                    item_id = int(view.kwargs.get('pk'))
                    
                    try:
                        item = MenuItem.objects.get(pk=item_id)
                    except MenuItem.DoesNotExist:
                        raise PermissionDenied(f"This Menu Item ID ({item_id}) is not valid!")

                    if item.restaurant.id == rest_id:
                        return True
                    raise PermissionDenied(f"The specified menu item ({item_id}) does not belong " +
                                            f"to the specified restaurant ({rest_id})!")

                raise PermissionDenied(f"This user does not own the specified restaurant ({rest_id})")

            raise PermissionDenied(f"This user is not a restaurant or admin user!")

        raise PermissionDenied("This user is not authenticated!")
    

class IsAuthAdminAndList(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        
        if is_authenticated and is_admin:
            if view.action == 'list':
                return True
            raise PermissionDenied(f"This action is not allowed ({view.action})!")
        
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated admin user!")