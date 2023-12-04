from rest_framework import serializers
from . import models
import restaurants.serializers as rs


class CalorieTrendsSerializer(serializers.ModelSerializer):
    calorie_level = serializers.CharField(source='get_calorie_level_display')
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.CalorieTrends
        fields = '__all__'


class RestrictionTagTrendsSerializer(serializers.ModelSerializer):
    tag = rs.RestrictionTagSerializer()
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.RestrictionTagTrends
        fields = '__all__'


class AllergyTagTrendsSerializer(serializers.ModelSerializer):
    tag = rs.AllergyTagSerializer()
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.AllergyTagTrends
        fields = '__all__'


class IngredientTagTrendsSerializer(serializers.ModelSerializer):
    tag = rs.IngredientTagSerializer()
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.IngredientTagTrends
        fields = '__all__'


class TasteTagTrendsSerializer(serializers.ModelSerializer):
    tag = rs.TasteTagSerializer()
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.TasteTagTrends
        fields = '__all__'


class CookStyleTagTrendsSerializer(serializers.ModelSerializer):
    tag = rs.CookStyleTagSerializer()
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.CookStyleTagTrends
        fields = '__all__'


class MenuItemPerformanceTrendsSerializer(serializers.ModelSerializer):
    item = rs.MenuItemNameSerializer()
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.MenuItemPerformanceTrends
        fields = '__all__'


class AppSatisfactionTrendsSerializer(serializers.ModelSerializer):
    trend_type = serializers.CharField(source='get_trend_type_display')
    
    class Meta:
        model = models.AppSatisfactionTrends
        fields = '__all__'