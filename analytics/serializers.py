from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
import restaurants.serializers as rs
import restaurants.models as rm

User = get_user_model()


# Made the only serializers available to be the GET-styled serializers


class GlobalAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GlobalAnalytics
        fields = '__all__'


# Calorie Analytics Serializers
class CalorieAnalyticsSerializer(serializers.ModelSerializer):
    LEVEL_CALORIE = [
        (0, 'Invalid'),(1, "0 - 199"), (2, '200 - 399'), (3 , '400 - 599'), 
        (4, '600 - 799'), (5, '800 - 999'), (6, '1000 - 1199'),
        (7,'1200 - 1399'),(8,'1400 - 1599'),(9, '1600 - 1799'),
        (10, '1800 - 1999'), (11, '2000 and up')
    ]

    calorie_level = serializers.ChoiceField(choices=LEVEL_CALORIE)

    class Meta:
        model = models.CalorieAnalytics
        fields = ['id', 'calorie_level', 'number_of_profiles', 'number_of_menuItems', 'date_stamp']


# Restriction Tag Analytics Serializers    
class RestrictionTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.RestrictionTagSerializer()

    class Meta:
        model = models.RestrictionTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']


# Allergy Tag Analytics Serializers
class AllergiesTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.AllergyTagSerializer()

    class Meta:
        model = models.AllergiesTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']


# Ingredient Tag Analytics Serializers
class IngredientTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.IngredientTagSerializer()

    class Meta:
        model = models.IngredientTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']
    

# Taste Tag Analytics Serializers
class TasteTagAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.TasteTagSerializer()

    class Meta:
        model = models.TasteTagAnalytics
        fields = ['id', 'tag_id', 'number_of_patronProfile', 'number_of_menuItem', 'date_stamp']


# Cook Style Analytics Serializers
class CookStyleAnalyticsSerializer(serializers.ModelSerializer):
    tag_id = rs.CookStyleTagSerializer()

    class Meta:
        model = models.CookStyleAnalytics
        fields = ['id', 'tag_id', 'number_of_menuItem', 'date_stamp']


# Menu Item Performance Analytics Serializers
class MenuItemPerformanceAnalyticsSerializer(serializers.ModelSerializer):
    menuItem_id = rs.MenuItemGetSerializer()    # Should we use this or MenuItemListSerializer (only basic info not tags?)
    #menuItem_id = rs.MenuItemSerializer()      # Or this because it would return everything but with tag IDs
    average_rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )

    class Meta:
        model = models.MenuItemPerformanceAnalytics
        fields = ['id', 'menuItem_id', 'number_of_ratings', 'average_rating', 'date_stamp']
        

# App satisfaction serializers
class AppSatisfactionAnalyticsSerializer(serializers.ModelSerializer):
    average_rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )

    class Meta:
        model = models.AppSatisfactionAnalytics
        fields = '__all__'







# Made the only serializers available to be the GET-styled serializers
# So commented out the others

# class CalorieAnalyticsSerializer(serializers.ModelSerializer):
#     LEVEL_CALORIE = [
#         (0, 'Invalid'),(1, "0 - 199"), (2, '200 - 399'), (3 , '400 - 599'), 
#         (4, '600 - 799'), (5, '800 - 999'), (6, '1000 - 1199'),
#         (7,'1200 - 1399'),(8,'1400 - 1599'),(9, '1600 - 1799'),
#         (10, '1800 - 1999'), (11, '2000 and up')
#     ]

#     calorie_level = serializers.IntegerField(default=0)

#     class Meta:
#         model = models.CalorieAnalytics
#         fields = '__all__'


# class RestrictionTagAnalyticsSerializer(serializers.ModelSerializer):
#     tag_id = serializers.PrimaryKeyRelatedField(queryset = rm.RestrictionTag.objects.all())

#     class Meta:
#         model = models.RestrictionTagAnalytics
#         fields = '__all__'


# class AllergiesTagAnalyticsSerializer(serializers.ModelSerializer):
#     tag_id = serializers.PrimaryKeyRelatedField(queryset=rm.AllergyTag.objects.all())

#     class Meta:
#         model = models.AllergiesTagAnalytics
#         fields = '__all__'


# class IngredientTagAnalyticsSerializer(serializers.ModelSerializer):
#     tag_id = serializers.PrimaryKeyRelatedField(queryset=rm.IngredientTag.objects.all())

#     class Meta:
#         model = models.IngredientTagAnalytics
#         fields = '__all__'


# class TasteTagAnalyticsSerializer(serializers.ModelSerializer):
#     tag_id = serializers.PrimaryKeyRelatedField(queryset=rm.TasteTag.objects.all())

#     class Meta:
#         model = models.TasteTagAnalytics
#         fields = '__all__'


# class CookStyleAnalyticsSerializer(serializers.ModelSerializer):
#     tag_id = serializers.PrimaryKeyRelatedField(queryset=rm.CookStyleTag.objects.all())

#     class Meta:
#         model = models.CookStyleAnalytics
#         fields = '__all__'


# class MenuItemPerformanceAnalyticsSerializer(serializers.ModelSerializer):
#     menuItem_id = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())
#     average_rating = serializers.DecimalField(
#         max_digits=8,  # Total number of digits
#         decimal_places=2,  # Maximum of 2 decimal places
#     )

#     class Meta:
#         model = models.MenuItemPerformanceAnalytics
#         fields = '__all__'


# class AppSatisfactionGetSerializer(serializers.ModelSerializer):
#     average_rating = models.DecimalField(
#         max_digits=8,  # Total number of digits
#         decimal_places=2,  # Maximum of 2 decimal places
#     )

#     class Meta:
#         model = models.AppSatisfactionAnalytics
#         fields = '__all__'