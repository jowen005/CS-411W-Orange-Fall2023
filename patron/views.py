from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status, viewsets

from . import models, serializers, permissions
from restaurants.models import RestrictionTag, AllergyTag, TasteTag, IngredientTag, MenuItem
from restaurants.serializers import MenuItemListSerializer

# Create your views here.

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
        #Call Search function with self.request.data which returns menu item IDs
        search_results = [1, 2, 3]
        print(f'\n\n{search_results}\n\n')

        #If search was ok
        if len(search_results) > 0:
            history_serializer = self.get_serializer(data=request.data)
            history_serializer.is_valid(raise_exception=True)
            history_serializer.save(patron=self.request.user)

            objects = MenuItem.objects.filter(id__in=search_results)
            print(f'\n\n{objects}\n\n')
            menu_item_serializer = MenuItemListSerializer(objects, many=True)
            print(f'\n\n{menu_item_serializer.data}\n\n')

            response_data = {
                'message': ' Search successfully performed.',
                'results': menu_item_serializer.data,
            }

            print(f'\n\n{response_data}\n\n')

            status_code = status.HTTP_201_CREATED
            
            return Response(response_data, status=status_code)
        
        response_data = {'message': 'Search Failed'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


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




# @api_view(http_method_names=['GET'])
# def tag_overview(request:Request):
    
#     patrons =  models.Patron.objects.all()
#     allergies = AllergyTag.objects.all()
#     restrictions = RestrictionTag.objects.all()
#     tastes = TasteTag.objects.all()
    
#     response = {"AllergyTag": {},"RestrictionTag":{},"TasteTag":{}}
#     for allergy in allergies:
#         response["AllergyTag"][str(allergy.id)] = {"title":allergy.title,"count":0}

#     for restriction in restrictions:
#         response["RestrictionTag"][str(restriction.id)] = {"title":restriction.id, "count":0}

#     for taste in tastes:
#         response["TasteTag"][str(taste.id)] = {"title":taste.id, "count":0}

#     for patron in patrons:
#         for tag_id in list(patron.patron_allergy_tag.values_list("id",flat=True)):
#             response["AllergyTag"][str(tag_id)]["count"] += 1
#         for tag_id in list(patron.patron_restriction_tag.values_list("id",flat=True)):
#             response["RestrictionTag"][str(tag_id)]["count"] += 1
#         for tag_id in list(patron.patron_taste_tag.values_list("id",flat=True)):
#             response["TasteTag"][str(tag_id)]["count"] += 1
        
#     return Response(data=response, status=status.HTTP_200_OK)