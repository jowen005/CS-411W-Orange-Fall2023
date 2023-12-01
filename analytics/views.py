from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, views
from django.core.management import call_command
from django.shortcuts import get_object_or_404

from . import models, serializers, permissions
from .utils import calorie_analysis, global_analysis, menu_item_analysis, tag_analysis, satisfaction_analysis
import restaurants.models as rm


class GlobalAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAdminAndList]
    serializer_class = serializers.GlobalAnalyticsSerializer

    def get_queryset(self):
        try:
            return [models.GlobalAnalytics.objects.latest('date_stamp')]
        except models.GlobalAnalytics.DoesNotExist:
            return models.GlobalAnalytics.objects.none()


class CalorieAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthNotPatronAndReadOnly]
    serializer_class = serializers.CalorieAnalyticsSerializer

    def get_queryset(self):

        try:
            latest_datestamp = models.CalorieAnalytics.objects.latest('date_stamp').date_stamp
        except models.CalorieAnalytics.DoesNotExist:
            return models.CalorieAnalytics.objects.none()

        queryset = models.CalorieAnalytics.objects.filter(
            date_stamp=latest_datestamp
        ).order_by('calorie_level')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        calorie_level = int(kwargs.get('pk'))

        if calorie_level < 1 or calorie_level > 11:
            response = {
                'message': 'Supplied Calorie Level must be within the range 1 to 11 inclusive!'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        
        # instance = models.CalorieAnalytics.objects.filter(calorie_level=calorie_level).latest('date_stamp')
        queryset = self.get_queryset()
        analytic_obj = queryset.filter(calorie_level=calorie_level).first()
        if analytic_obj is None:
            response = {
                'message': f'This Calorie Level ({calorie_level}) is valid but does not yet have analytics!'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(analytic_obj)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = None
    AnalyticsModel = None
    TagModel = None
    
    def get_queryset(self):

        try:
            latest_datestamp = self.AnalyticsModel.objects.latest('date_stamp').date_stamp
        except self.AnalyticsModel.DoesNotExist:
            return self.AnalyticsModel.objects.none()

        queryset = self.AnalyticsModel.objects.filter(
            date_stamp=latest_datestamp
        ).order_by('tag_id')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        tag_id = int(kwargs.get('pk'))

        valid_ids = self.TagModel.objects.all().values_list('id', flat=True)
        if tag_id not in valid_ids:
            response = {
                'message': f'This Tag ID ({tag_id}) is not valid!'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        analytic_obj = queryset.filter(tag_id__id=tag_id).first()
        if analytic_obj is None:
            response = {
                'message': f'This Tag ID ({tag_id}) is valid but does not yet have analytics!'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(analytic_obj)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RestrictionTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthNotPatronAndReadOnly]
    serializer_class = serializers.RestrictionTagAnalyticsSerializer
    AnalyticsModel = models.RestrictionTagAnalytics
    TagModel = rm.RestrictionTag


class AllergiesTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthNotPatronAndReadOnly]
    serializer_class = serializers.AllergiesTagAnalyticsSerializer
    AnalyticsModel = models.AllergiesTagAnalytics
    TagModel = rm.AllergyTag
        

class IngredientTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthNotPatronAndReadOnly]
    serializer_class = serializers.IngredientTagAnalyticsSerializer
    AnalyticsModel = models.IngredientTagAnalytics
    TagModel = rm.IngredientTag
        

class TasteTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthNotPatronAndReadOnly]
    serializer_class = serializers.TasteTagAnalyticsSerializer
    AnalyticsModel = models.TasteTagAnalytics
    TagModel = rm.TasteTag
    

class CookStyleAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthNotPatronAndReadOnly]
    serializer_class = serializers.CookStyleAnalyticsSerializer
    AnalyticsModel = models.CookStyleAnalytics
    TagModel = rm.CookStyleTag
        

# Where You specify the menu items for a specific restaurant location using 'restaurant id'
class LocalMenuItemPerformanceViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.LocalMenuItemPermission]
    serializer_class = serializers.MenuItemPerformanceAnalyticsSerializer

    # Restaurant Specific Menu Items
    def get_queryset(self):

        requested_id = self.kwargs.get('restaurant_id')
        restaurant = rm.Restaurant.objects.get(pk=requested_id)

        try:
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
            ).latest('date_stamp').date_stamp
        except models.MenuItemPerformanceAnalytics.DoesNotExist: # No Analytics for a Restaurant
            return models.MenuItemPerformanceAnalytics.objects.none()

        queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
                date_stamp=latest_datestamp
        ).order_by('menuItem_id')

        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        item_id = int(kwargs.get('pk'))

        # The permission class verifies the existence of the 'item_id'
        
        queryset = self.get_queryset()
        analytic_obj = queryset.filter(menuItem_id__id=item_id).first()
        if analytic_obj is None:
            response = {
                'message': f'This Menu Item ({item_id}) is valid but does not yet have analytics!'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(analytic_obj)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

# All Menu Items for the Admin Only?
class GlobalMenuItemPerformanceViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAdminAndReadOnly]
    serializer_class = serializers.MenuItemPerformanceAnalyticsSerializer

    def get_queryset(self):

        try:
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
        except models.MenuItemPerformanceAnalytics.DoesNotExist: # No Analytics At All
            return models.MenuItemPerformanceAnalytics.objects.none()

        queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                date_stamp=latest_datestamp
        ).order_by('menuItem_id')

        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        item_id = int(kwargs.get('pk'))

        valid_ids = rm.MenuItem.objects.all().values_list('id', flat=True)

        if item_id not in valid_ids:
            response = {
                'message': f'This Menu Item ID ({item_id}) is not valid!'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset()
        analytic_obj = queryset.filter(menuItem_id__id=item_id).first()
        if analytic_obj is None:
            response = {
                'message': f'This Menu Item ({item_id}) is valid but does not yet have analytics!'
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(analytic_obj)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

class AppSatisfactionAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAdminAndList]
    serializer_class = serializers.AppSatisfactionAnalyticsSerializer

    def get_queryset(self):
        try:
            return [models.AppSatisfactionAnalytics.objects.latest('date_stamp')]
        except models.AppSatisfactionAnalytics.DoesNotExist:
            return models.AppSatisfactionAnalytics.objects.none()
        
class LocalRestaurantAnalyticsViewset(viewsets.ModelViewSet):
        permission_classes = [permissions.LocalRestaurantAnalyticsPermission]
        serializer_class = serializers.LocalRestaurantAnalyticsSerializer

        def get_queryset(self):
            requested_id = self.kwargs.get('restaurant_id')
            restaurant = rm.Restaurant.objects.get(pk=requested_id)

            try:
                latest_datestamp = models.LocalRestaurantAnalytics.objects.filter(
                    restaurant_id_restaurant=restaurant,
                ).latest('date_stamp').date_stamp
            except models.LocalRestaurantAnalytics.DoesNotExist: # No Analytics for a Restaurant
                return models.LocalRestaurantAnalytics.objects.none()

            queryset = models.LocalRestaurantAnalytics.objects.filter(
                restaurant_id_restaurant=restaurant,
                date_stamp=latest_datestamp
            ).order_by('restaurant_id')

            return queryset
        
        def retrieve(self, request, *args, **kwargs):
            requested_id = int(kwargs.get('pk'))

            # The permission class verifies the existence of the 'restaurantd_id'
        
            queryset = self.get_queryset()
            analytic_obj = queryset.filter(restaurant_id__id=requested_id).first()
            if analytic_obj is None:
                response = {
                    'message': f'This Restaurant({requested_id}) is valid but does not yet have analytics!'
            }
                return Response(data=response, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(analytic_obj)

            return Response(data=serializer.data, status=status.HTTP_200_OK)


class ManualAnalyticsCommandView(views.APIView):
    permission_classes = [permissions.IsAuthAdminAndCreate]

    def post(self, request, *args, **kwargs):
        call_command('manualAnalytics')

        return Response({'detail':'manualAnalytics was triggered successfully.'}, status=status.HTTP_200_OK)