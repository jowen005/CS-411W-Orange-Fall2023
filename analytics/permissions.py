from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS)
from restaurants.models import Restaurant, MenuItem
from rest_framework.exceptions import PermissionDenied


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
    

class IsNotPatronAndList(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated 
        is_not_patron = request.user.user_type != 'patron'
        
        if is_authenticated and is_not_patron:
            if view.action == 'list':
                return True
            raise PermissionDenied(f"This action is not allowed ({view.action})!")
        
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated admin or restaurant user!")
    

class IsAuthAdminAndReadOnly(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        
        if is_authenticated and is_admin:
            if view.action == 'list' or view.action == 'retrieve':
                return True
            raise PermissionDenied(f"This action is not allowed ({view.action})!")
        
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated admin user!")
    

class IsAuthNotPatronAndReadOnly(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated and (is_admin or is_restaurant):
            if view.action == 'list' or view.action == 'retrieve':
                return True
            raise PermissionDenied(f"This action is not allowed ({view.action})!")
        
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated restaurant or admin user!")
    

class LocalMenuItemPermission(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated:
            if is_admin:
                if view.action == 'list':
                    return True
                elif view.action == 'retrieve':
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

                else:
                    raise PermissionDenied(f"This action is not allowed ({view.action})!")
            
            if is_restaurant:
                owned_rest_ids = list(Restaurant.objects.filter(owner=request.user).values_list('id',flat=True))
                rest_id = view.kwargs.get('restaurant_id')
                
                if rest_id in owned_rest_ids:
                    if view.action == 'list':
                        return True
                    elif view.action == 'retrieve':
                        item_id = int(view.kwargs.get('pk'))
                        
                        try:
                            item = MenuItem.objects.get(pk=item_id)
                        except MenuItem.DoesNotExist:
                            raise PermissionDenied(f"This Menu Item ID ({item_id}) is not valid!")

                        if item.restaurant.id == rest_id:
                            return True
                        raise PermissionDenied(f"The specified menu item ({item_id}) does not belong " +
                                               f"to the specified restaurant ({rest_id})!")
                    
                    raise PermissionDenied(f"This action is not allowed ({view.action})!")

                raise PermissionDenied(f"This user does not own the specified restaurant ({rest_id})")

            raise PermissionDenied(f"This user is not a restaurant or admin user!")

        raise PermissionDenied("This user is not authenticated!")
    
class LocalRestaurantAnalyticsPermission(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated 
        is_admin = request.user.user_type == 'admin'
        is_restaurant = request.user.user_type == 'restaurant'
        
        if is_authenticated:
            if is_admin:
                if view.action == 'list':
                    return True
                # elif view.action == 'retrieve':
                #     rest_id = view.kwargs.get('restaurant_id')
                #     restaurant_id = int(view.kwargs.get('pk'))

                #     try:
                #         restaurant = Restaurant.objects.get(pk=restaurant_id)
                #     except Restaurant.DoesNotExist:
                #         raise PermissionDenied(f"This Restaurant ID ({restaurant_id}) is not valid!")
                    
                #     if restaurant.owner == rest_id:
                #         return True
                #     raise PermissionDenied(f"The specified restaurant ({restaurant_id}) does not belong " +
                #                            f"to the specified restaurant ({rest_id})!")

                else:
                    raise PermissionDenied(f"This action is not allowed ({view.action})!")
            
            if is_restaurant:
                owned_rest_ids = list(Restaurant.objects.filter(owner=request.user).values_list('id',flat=True))
                rest_id = view.kwargs.get('restaurant_id')
                
                if rest_id in owned_rest_ids:
                    if view.action == 'list':
                        return True
                    # elif view.action == 'retrieve':
                    #     restaurant_id = int(view.kwargs.get('pk'))
                        
                    #     try:
                    #         restaurant = Restaurant.objects.get(pk=restaurant_id)
                    #     except Restaurant.DoesNotExist:
                    #         raise PermissionDenied(f"This Restaurant ID ({restaurant_id}) is not valid!")

                    #     if Restaurant.owner == rest_id:
                    #         return True
                    #     raise PermissionDenied(f"The specified restaurant ({restaurant_id}) does not belong " +
                    #                            f"to the specified restaurant ({rest_id})!")
                    
                    raise PermissionDenied(f"This action is not allowed ({view.action})!")

                raise PermissionDenied(f"This user does not own the specified restaurant ({rest_id})")

            raise PermissionDenied(f"This user is not a restaurant or admin user!")

        raise PermissionDenied("This user is not authenticated!")
    

class IsAuthAdminAndCreate(BasePermission):
    def has_permission(self,request,view):
        is_authenticated = request.user.is_authenticated
        is_admin = request.user.user_type == 'admin'

        if is_authenticated and is_admin:
            if request.method == 'POST':
                return True
            raise PermissionDenied(f"This request method is not allowed ({request.method})!")
            
        raise PermissionDenied(f"This user ({request.user.user_type}) is not an " +
                               f"authenticated admin user!")
    


        
    
