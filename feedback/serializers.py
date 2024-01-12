from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
import restaurants.serializers as rs
import restaurants.models as rm


User = get_user_model()

# Serializer for combined Review model
class ReviewsGetSerializer(serializers.ModelSerializer):
    patron_name = serializers.CharField(max_length = 255)
    menu_item = rs.MenuItemListSerializer()
    
    review = serializers.CharField(max_length=255)
    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['patron_name']

class ReviewsSerializer(serializers.ModelSerializer):
    
    menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())
    
    review = serializers.CharField(max_length=255)
    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.Reviews
        fields = '__all__'
        read_only_fields = ['patron']
        

class AppSatisfactionSerializer(serializers.ModelSerializer):
    review = serializers.CharField(max_length=255)

    rating = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )

    class Meta:
        model = models.AppSatisfaction
        fields = '__all__'
        read_only_fields = ['user']

