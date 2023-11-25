from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics, views
from django.http import HttpRequest

from . import models, serializers, permissions
from .utils import calorie_analysis, global_analysis, menu_item_analysis, tag_analysis, satisfaction_analysis
import restaurants.models as rm


class GlobalAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndAdminAndList]
    serializer_class = serializers.GlobalAnalyticsSerializer

    def get_queryset(self):
        try:
            return models.GlobalAnalytics.objects.latest('date_stamp')
        except models.GlobalAnalytics.DoesNotExist:
            global_analysis.driver()
            return models.GlobalAnalytics.objects.latest('date_stamp')
        

class CalorieAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.CalorieAnalyticsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.CalorieAnalytics.objects.latest('date_stamp')
            return models.CalorieAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('calorie_level')
        except models.CalorieAnalytics.DoesNotExist:
            calorie_analysis.driver()
            latest_datestamp = models.CalorieAnalytics.objects.latest('date_stamp')
            return models.CalorieAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('calorie_level')
        

class RestrictionTagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.RestrictionTagAnalyticsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.RestrictionTagAnalytics.objects.latest('date_stamp')
            return models.RestrictionTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        except models.RestrictionTagAnalytics.DoesNotExist:
            tag_analysis.driver(restriction=True)
            latest_datestamp = models.RestrictionTagAnalytics.objects.latest('date_stamp')
            return models.RestrictionTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        

class AllergiesTagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.AllergiesTagAnalyticsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.AllergiesTagAnalytics.objects.latest('date_stamp')
            return models.AllergiesTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        except models.AllergiesTagAnalytics.DoesNotExist:
            tag_analysis.driver(allergy=True)
            latest_datestamp = models.AllergiesTagAnalytics.objects.latest('date_stamp')
            return models.AllergiesTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        

class IngredientTagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.IngredientTagAnalyticsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.IngredientTagAnalytics.objects.latest('date_stamp')
            return models.IngredientTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        except models.IngredientTagAnalytics.DoesNotExist:
            tag_analysis.driver(ingredient=True)
            latest_datestamp = models.IngredientTagAnalytics.objects.latest('date_stamp')
            return models.IngredientTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        

class TasteTagAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.TasteTagAnalyticsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.TasteTagAnalytics.objects.latest('date_stamp')
            return models.TasteTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        except models.TasteTagAnalytics.DoesNotExist:
            tag_analysis.driver(taste=True)
            latest_datestamp = models.TasteTagAnalytics.objects.latest('date_stamp')
            return models.TasteTagAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        

class CookStyleAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndNotPatronAndList]
    serializer_class = serializers.CookStyleAnalyticsSerializer

    def get_queryset(self):
        try:
            latest_datestamp = models.CookStyleAnalytics.objects.latest('date_stamp')
            return models.CookStyleAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        except models.CookStyleAnalytics.DoesNotExist:
            tag_analysis.driver(cook_style=True)
            latest_datestamp = models.CookStyleAnalytics.objects.latest('date_stamp')
            return models.CookStyleAnalytics.objects.filter(date_stamp=latest_datestamp).order_by('tag_id')
        

# Where You specify the menu items for a specific restaurant location using 'restaurant id'
class LocalMenuItemPerformanceViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.LocalMenuItemPermission]
    serializer_class = serializers.MenuItemPerformanceAnalyticsSerializer

    def get_queryset(self):
        user = self.request.user
        
        requested_id = self.kwargs.get('restaurant_id')
        restaurant = rm.Restaurant.objects.get(pk=requested_id)
        try:
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp')
            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
                date_stamp=latest_datestamp
            ).order_by('menuItem_id')

            if queryset.empty():
                raise models.MenuItemPerformanceAnalytics.DoesNotExist

        except models.MenuItemPerformanceAnalytics.DoesNotExist:
            #Call Menu_item_analysis for specific group of tags????
            menu_item_analysis.driver()
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp')
            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant=restaurant,
                date_stamp=latest_datestamp
            ).order_by('menuItem_id')

        return queryset

        
class GlobalMenuItemPerformanceViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.LocalMenuItemPermission]
    serializer_class = serializers.MenuItemPerformanceAnalyticsSerializer

    def get_queryset(self):
        user = self.request.user
        
        try:
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp')
            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant__owner=user,
                date_stamp=latest_datestamp
            ).order_by('menuItem_id')

            if queryset.empty():
                raise models.MenuItemPerformanceAnalytics.DoesNotExist

        except models.MenuItemPerformanceAnalytics.DoesNotExist:
            #Call Menu_item_analysis for specific group of tags????
            menu_item_analysis.driver()
            latest_datestamp = models.MenuItemPerformanceAnalytics.objects.latest('date_stamp')
            queryset = models.MenuItemPerformanceAnalytics.objects.filter(
                menuItem_id__restaurant__owner=user,
                date_stamp=latest_datestamp
            ).order_by('menuItem_id')

        return queryset
        

class AppSatisfactionAnalyticsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthAndAdminAndList]
    serializer_class = serializers.AppSatisfactionAnalyticsSerializer

    def get_queryset(self):
        try:
            return models.AppSatisfactionAnalytics.objects.latest('date_stamp')
        except models.AppSatisfactionAnalytics.DoesNotExist:
            satisfaction_analysis.driver()
            return models.AppSatisfactionAnalytics.objects.latest('date_stamp')