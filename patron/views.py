from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, viewsets
from .utils.search import advancedSearch
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, permission_classes

from . import models, serializers, permissions
from restaurants.models import MenuItem
from restaurants.serializers import MenuItemListSerializer
from feedback.models import Reviews

from patron.utils.generateSuggestions import generateSuggestions


class PatronViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthPatronAndIsUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.Patron.objects.filter(user=user)
        else:
            return models.Patron.objects.none()
        
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.PatronGetSerializer
        return serializers.PatronSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
	
    def perform_update(self, serializer):
        serializer.save(profile_updated=True)


class SearchHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthPatronIsUserNoUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.PatronSearchHistory.objects.filter(patron=user)
        else:
            return models.PatronSearchHistory.objects.none()
        
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.PatronSearchHistoryGetSerializer
        return serializers.PatronSearchHistorySerializer
    
    def create(self, request, *args, **kwargs):
        
        history_serializer = self.get_serializer(data=request.data)
            
        # Catch if Search object is invalid
        try:
            history_serializer.is_valid(raise_exception=True)
            history_serializer.save(patron=self.request.user)

        except ValidationError as e:
            response_data = {
                'message': 'Invalid input data.',
                'errors': e.detail,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # Format Search for entry to the search function
        instance = history_serializer.instance
        search_obj = history_serializer.data
        search_obj['search_datetime'] = instance.search_datetime
        search_obj.pop('id')
        search_obj.pop('patron')
        search_obj.pop('calorie_level')

        print(f'\n\n{search_obj}\n\n')

        # 'query', 'calorie_limit', 'dietary_restriction_tags', 
        # 'allergy_tags', 'patron_taste_tags', 'disliked_ingredients', 
        # 'price_min', 'price_max', 'search_datetime'

        search_results = advancedSearch(**search_obj)

        # Handle if results were returned
        if len(search_results) > 0:
            
            objects = MenuItem.objects.filter(id__in=search_results)
            menu_item_serializer = MenuItemListSerializer(objects, many=True)
            
            response_data = {
                'message': ' Search successfully performed.',
                'results': menu_item_serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # Handle if no results were returned or search failed
        response_data = {
            'message': 'No Results'
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthPatronIsUserNoUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.Bookmark.objects.filter(patron=user)
        else:
            return models.Bookmark.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.BookmarkGetSerializer
        return serializers.BookmarkSerializer

    def perform_create(self, serializer):
        serializer.save(patron=self.request.user)


class MenuItemHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthPatronIsUserNoUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.MenuItemHistory.objects.filter(patron=user)
        else:
            return models.MenuItemHistory.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.MenuItemHistoryGetSerializer
        return serializers.MenuItemHistorySerializer

    def perform_create(self, serializer):
        serializer.save(patron=self.request.user)

    def create(self, request, *args, **kwargs):
        
        bookmarkid = request.data.pop("bookmarkid", 0)
        review = Reviews.objects.get(id=request.data['review'])

        if request.data['menu_item'] != review.menu_item.id:
            response_data = {
                'message': 'Menu Item referenced by review does not match supplied menu item.'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        history_serializer = self.get_serializer(data=request.data)
        
        # Catch if menu item history is invalid
        try:
            history_serializer.is_valid(raise_exception=True)

        except serializers.ValidationError as e:
            response_data = {
                'message': 'Invalid input data.',
                'errors': e.detail,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle if NOT adding from bookmarks
        if bookmarkid == 0:     # 0 is invalid ID, meaning not added from bookmarks
            history_serializer.save(patron=self.request.user)
            response_data = {
                'message': 'Successfully added to meal history.',
                'results': history_serializer.data,
            }
			#SAVE HERE NOTE =================================================================================================================================
            models.Patron.objects.get(user=request.user).save(profile_updated=True)
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        # Handle if adding from bookmarks
        else:
            # Catch if bookmark ID is invalid
            try:
                bookmark = models.Bookmark.objects.get(id=bookmarkid)

                # Handle if specified menu item is the same as menu item in bookmark
                if request.data["menu_item"] == bookmark.menu_item.id:
                    
                    bookmark.delete()
                    history_serializer.save(patron=self.request.user)

                    response_data = {
                        'message': 'Successfully added to meal history and removed from bookmarks.',
                        'results': history_serializer.data,
                    }
					#SAVE HERE NOTE =================================================================================================================================
                    models.Patron.objects.get(user=request.user).save(profile_updated=True)
                    return Response(response_data, status=status.HTTP_201_CREATED)
                
                else:
                    response_data = {
                        'message': 'Supplied menu item ID does not match bookmark',
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
            except models.Bookmark.DoesNotExist:
                response_data = {
                    'message': 'Bookmark not found with the specified bookmarkid.',
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as ex:
                response_data = {
                    'message': 'An error occurred while processing the request.',
                    'error': str(ex),
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['GET'])
@permission_classes([permissions.IsAuthPatron])
def SuggestionFeedAPI(request:Request):

    try:
        patron_id = models.Patron.objects.get(user=request.user).id
    except models.Patron.DoesNotExist:
        response_data = {
            'message': 'This user does not have a Patron Profile.',
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    suggestions = generateSuggestions(patron_id)
    serializer = MenuItemListSerializer(suggestions, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)