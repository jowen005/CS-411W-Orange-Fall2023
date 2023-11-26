from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics, views
from django.http import HttpRequest
from django.db.models import Max
from django.utils import timezone
from datetime import datetime

from . import models, serializers, permissions
from .utils import calorie_analysis, global_analysis, menu_item_analysis, tag_analysis, satisfaction_analysis
import restaurants.models as rm


class GlobalAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndAdminAndList]
    serializer_class = serializers.GlobalAnalyticsSerializer

    def get_queryset(self):
        try:
            return [models.GlobalAnalytics.objects.latest('date_stamp')]
        except models.GlobalAnalytics.DoesNotExist:
            global_analysis.driver()
            return [models.GlobalAnalytics.objects.latest('date_stamp')]
            # return models.GlobalAnalytics.objects.none()


class CalorieAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.CalorieAnalyticsSerializer

    def get_queryset(self):

        try:
            latest_datestamp = models.CalorieAnalytics.objects.latest('date_stamp').date_stamp
        except models.CalorieAnalytics.DoesNotExist:
            calorie_analysis.driver()
            latest_datestamp = models.CalorieAnalytics.objects.latest('date_stamp').date_stamp
            # return models.CalorieAnalytics.objects.none()

        queryset = models.CalorieAnalytics.objects.filter(
            date_stamp__gte=latest_datestamp
        ).order_by('calorie_level')
        
        return queryset


class TagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = None
    TagModel = None
    AnalyticsModel = None
    tag_type = None
    
    def get_queryset(self):

        try:
            latest_datestamp = self.AnalyticsModel.objects.latest('date_stamp').date_stamp
        except self.AnalyticsModel.DoesNotExist:
            tag_analysis.driver(**{f'{self.tag_type}':True})
            latest_datestamp = self.AnalyticsModel.objects.latest('date_stamp').date_stamp
            # return self.TagModel.objects.none()

        queryset = self.AnalyticsModel.objects.filter(
            date_stamp=latest_datestamp
        ).order_by('tag_id')
        
        return queryset


class RestrictionTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.RestrictionTagAnalyticsSerializer
    TagModel = rm.RestrictionTag
    AnalyticsModel = models.RestrictionTagAnalytics
    tag_type = 'restriction'


class AllergiesTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.AllergiesTagAnalyticsSerializer
    TagModel = rm.AllergyTag
    AnalyticsModel = models.AllergiesTagAnalytics
    tag_type = 'allergy'
        

class IngredientTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.IngredientTagAnalyticsSerializer
    TagModel = rm.IngredientTag
    AnalyticsModel = models.IngredientTagAnalytics
    tag_type = 'ingredient'
        

class TasteTagAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.TasteTagAnalyticsSerializer
    TagModel = rm.TasteTag
    AnalyticsModel = models.TasteTagAnalytics
    tag_type = 'taste'
    

class CookStyleAnalyticsViewset(TagAnalyticsViewset):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.CookStyleAnalyticsSerializer
    TagModel = rm.CookStyleTag
    AnalyticsModel = models.CookStyleAnalytics
    tag_type = 'cook_style'
        

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
            # TODO: Optimize for specific restaurant analytics
            menu_item_analysis.driver()
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
            ).latest('date_stamp').date_stamp
            # return models.MenuItemPerformanceAnalytics.objects.none()

        queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
                date_stamp__gte=latest_datestamp
        ).order_by('menuItem_id')

        return queryset

        
class GlobalMenuItemPerformanceViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.MenuItemPerformanceAnalyticsSerializer

    def get_queryset(self):
        
        user = self.request.user
        
        # RestProfile Specific Menu Items
        if user.user_type == 'restaurant':
            try:
                latest_datestamp = models.MenuItemPerformanceAnalytics.objects.filter(
                    menuItem_id__restaurant__owner=user,
                ).latest('date_stamp').date_stamp
            except models.MenuItemPerformanceAnalytics.DoesNotExist: # No Analytics for a RestProfile
                # TODO: Optimize for specific restaurant profile analytics
                menu_item_analysis.driver()
                latest_datestamp = models.MenuItemPerformanceAnalytics.objects.filter(
                    menuItem_id__restaurant__owner=user,
                ).latest('date_stamp').date_stamp
                # return models.MenuItemPerformanceAnalytics.objects.none()

            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                    menuItem_id__restaurant__owner=user,
                    date_stamp__gte=latest_datestamp
            ).order_by('menuItem_id')

        # All Menu Items
        elif user.user_type == 'admin':
            try:
                latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
            except models.MenuItemPerformanceAnalytics.DoesNotExist: # No Analytics At All
                menu_item_analysis.driver()
                latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
                # return models.MenuItemPerformanceAnalytics.objects.none()

            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                    date_stamp__gte=latest_datestamp
            ).order_by('menuItem_id')

        return queryset
        

class AppSatisfactionAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndAdminAndList]
    serializer_class = serializers.AppSatisfactionAnalyticsSerializer

    def get_queryset(self):
        try:
            return [models.AppSatisfactionAnalytics.objects.latest('date_stamp')]
        except models.AppSatisfactionAnalytics.DoesNotExist:
            satisfaction_analysis.driver()
            return [models.AppSatisfactionAnalytics.objects.latest('date_stamp')]
            # return models.AppSatisfactionAnalytics.objects.none()