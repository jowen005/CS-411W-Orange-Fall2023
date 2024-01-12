from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
import restaurants.serializers as rs

User = get_user_model()

# Made the only serializers available to be the GET-styled serializers

class GlobalAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GlobalAnalytics
        fields = '__all__'


class CalorieAnalyticsSerializer(serializers.ModelSerializer):
    LEVEL_CALORIE = [
        (0, 'Invalid'),(1, "0 - 199"), (2, '200 - 399'), (3 , '400 - 599'), 
        (4, '600 - 799'), (5, '800 - 999'), (6, '1000 - 1199'),
        (7,'1200 - 1399'),(8,'1400 - 1599'),(9, '1600 - 1799'),
        (10, '1800 - 1999'), (11, '2000 and up')
    ]
    
    calorie_name = serializers.CharField(source='get_calorie_level_display')

    class Meta:
        model = models.CalorieAnalytics
        fields = ['id', 'calorie_level', 'calorie_name', 'number_of_profiles', 'number_of_menuItems', 'date_stamp']

 
class RestrictionTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.RestrictionTagSerializer()

    class Meta:
        model = models.RestrictionTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']


class AllergiesTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.AllergyTagSerializer()

    class Meta:
        model = models.AllergiesTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']


class IngredientTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.IngredientTagSerializer()

    class Meta:
        model = models.IngredientTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']
    

class TasteTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.TasteTagSerializer()

    class Meta:
        model = models.TasteTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']


class CookStyleAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.CookStyleTagSerializer()

    class Meta:
        model = models.CookStyleAnalytics
        fields = ['id', 'tag_id', 'number_of_menuItem', 'date_stamp']


class OverallFilterAnalyticsSerializer(serializers.ModelSerializer):
    filter_type = serializers.CharField(source='get_filter_type_display')

    class Meta:
        model = models.OverallFilterAnalytics
        fields = '__all__'


class MenuItemPerformanceAnalyticsSerializer(serializers.ModelSerializer):
    menuItem_id = rs.MenuItemNameSerializer()
    average_rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )

    class Meta:
        model = models.MenuItemPerformanceAnalytics
        # fields = '__all__'
        exclude = ['number_of_added_to_History']
        # fields = ['id', 'menuItem_id', 'number_of_ratings', 'average_rating', 'date_stamp']
        

class AppSatisfactionAnalyticsSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )

    class Meta:
        model = models.AppSatisfactionAnalytics
        fields = '__all__'


class LocalRestaurantAnalyticsSerializer(serializers.ModelSerializer):
    restaurant_id = rs.RestaurantListSerializer()
    
    class Meta:
        model = models.LocalRestaurantAnalytics
        fields = '__all__'


class LoginAnalyticsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)

    class Meta:
        model = models.LoginAnalytics
        exclude = ['user']

