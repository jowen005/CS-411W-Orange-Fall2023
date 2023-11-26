from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics, views
from django.http import HttpRequest
from django.db.models import Max

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


class CalorieAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.CalorieAnalyticsSerializer

    def get_queryset(self):

        while True:
            latest_datestamps = models.CalorieAnalytics.objects.values('calorie_level').annotate(
                latest_date=Max('date_stamp')
            ).distinct()
        
            if len(latest_datestamps) != 11:
                calorie_analysis.driver()
            else:
                break
        
        earliest_datestamp = min(obj['latest_date'] for obj in latest_datestamps)

        queryset = models.CalorieAnalytics.objects.filter(
            date_stamp__gte=earliest_datestamp
        ).order_by('calorie_level')
        
        return queryset


class TagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = None
    TagModel = None
    AnalyticsModel = None
    tag_type = None
    
    def get_queryset(self):

        num_of_tags = self.TagModel.objects.all().count()

        while True:
            latest_datestamps = self.AnalyticsModel.objects.values('tag_id').annotate(
                latest_date=Max('date_stamp')
            ).distinct()
        
            if len(latest_datestamps) != num_of_tags:
                tag_analysis.driver(**{f'{self.tag_type}':True})
            else:
                break
        
        earliest_datestamp = min(obj['latest_date'] for obj in latest_datestamps)

        queryset = self.AnalyticsModel.objects.filter(
            date_stamp__gte=earliest_datestamp
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

    def get_queryset(self):

        requested_id = self.kwargs.get('restaurant_id')
        restaurant = rm.Restaurant.objects.get(pk=requested_id)

        num_of_items = rm.MenuItem.objects.filter(restaurant=restaurant).count()

        while True:
            latest_datestamps = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
            ).values('menuItem_id').annotate(
                latest_date=Max('date_stamp')
            ).distinct()
        
            if len(latest_datestamps) != num_of_items:
                #Call Menu_item_analysis for specific group of tags????
                menu_item_analysis.driver()
            else:
                break
        
        earliest_datestamp = min(obj['latest_date'] for obj in latest_datestamps)

        queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
                date_stamp__gte=earliest_datestamp
        ).order_by('menuItem_id')

        return queryset

        
class GlobalMenuItemPerformanceViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.MenuItemPerformanceAnalyticsSerializer

    def get_queryset(self):
        
        user = self.request.user
        
        if user.user_type == 'restaurant':
            num_of_items = rm.MenuItem.objects.filter(restaurant__owner=user).count()

            while True:
                latest_datestamps = models.MenuItemPerformanceAnalytics.objects.filter(
                    menuItem_id__restaurant__owner=user,
                ).values('menuItem_id').annotate(
                    latest_date=Max('date_stamp')
                ).distinct()
            
                if len(latest_datestamps) != num_of_items:
                    #Call Menu_item_analysis for specific group of tags????
                    menu_item_analysis.driver()
                else:
                    break
            
            earliest_datestamp = min(obj['latest_date'] for obj in latest_datestamps)

            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                    menuItem_id__restaurant__owner=user,
                    date_stamp__gte=earliest_datestamp
            ).order_by('menuItem_id')

        elif user.user_type == 'admin':
            num_of_items = rm.MenuItem.objects.all().count()

            while True:
                latest_datestamps = models.MenuItemPerformanceAnalytics.objects.values('menuItem_id').annotate(
                    latest_date=Max('date_stamp')
                ).distinct()
            
                if len(latest_datestamps) != num_of_items:
                    #Call Menu_item_analysis for specific group of tags????
                    menu_item_analysis.driver()
                else:
                    break
            
            earliest_datestamp = min(obj['latest_date'] for obj in latest_datestamps)

            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                    date_stamp__gte=earliest_datestamp
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