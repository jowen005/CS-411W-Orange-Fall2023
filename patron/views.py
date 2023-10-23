from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status, viewsets

from . import models, serializers, permissions
from restaurants.models import RestrictionTag, AllergyTag, TasteTag, IngredientTag, MenuItem
from restaurants.serializers import MenuItemListSerializer

# Create your views here.

class PatronViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatronSerializer
    permission_classes = [permissions.IsAuthPatronAndIsUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.Patron.objects.filter(user=user)
        else:
            return models.Patron.objects.none()
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatronSearchHistorySerializer
    permission_classes = [permissions.IsAuthPatronIsUserNoUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.PatronSearchHistory.objects.filter(patron=user)
        else:
            return models.PatronSearchHistory.objects.none()
    
    def perform_create(self, serializer):
        #Call Search function with self.request.data which returns menu item IDs
        search_results = [1, 2, 3]

        #If search was ok
        if len(search_results) > 0:
            serializer.save(patron=self.request.user)

            objects = MenuItem.objects.filter(id__in=search_results)
            menu_item_serializer = MenuItemListSerializer(objects, many=True)

            response_data = {
                'message': ' Search successfully performed.',
                'results': menu_item_serializer.data,
            }

            status_code = status.HTTP_201_CREATED
            
            return Response(response_data, status=status_code)
        
        response_data = {'message': 'Search Failed'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [permissions.IsAuthPatronIsUserNoUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.Bookmark.objects.filter(patron=user)
        else:
            return models.Bookmark.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MealHistorySerializer
    permission_classes = [permissions.IsAuthPatronIsUserNoUpdate]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patron':
            return models.MealHistory.objects.filter(patron=user)
        else:
            return models.MealHistory.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




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