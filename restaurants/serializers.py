from rest_framework import serializers
from . import models

class RestTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    
    class Meta:
        model = models.RestTag
        fields = ['id', 'title']

class RestaurantSerializer():
    pass

class RestOpenHourSerializer():
    pass
    
class FoodTypeTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.FoodTypeTag
        fields = ['id', 'title']

class CookStyleTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.CookStyleTag
        fields = ['id', 'title']

class TasteTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.TasteTag
        fields = ['id', 'title']

class MenuItemSerializer():
    pass