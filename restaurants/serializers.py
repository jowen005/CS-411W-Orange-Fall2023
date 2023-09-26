from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RestTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    
    class Meta:
        model = models.RestTag
        fields = ['id', 'title']


class RestaurantSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name = serializers.CharField(max_length=100)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    tags = serializers.PrimaryKeyRelatedField(queryset=models.RestTag.objects.all(),many=True)
    price_level = serializers.ChoiceField(choices=[
        ('$','$'),
        ('$$','$$'),
        ('$$$','$$$'),
    ])
    phone_number = serializers.CharField(max_length=12)
    
    street_name = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=30)
    state = serializers.CharField(max_length=2)
    zip_code = serializers.CharField(max_length=5)

    class Meta:
        model = models.Restaurant
        fields = ['id','owner','name','rating','tags','price_level',
                'phone_number','website', 'street_name','city','state','zip_code']
        read_only_fields = ['owner']


class RestOpenHourSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RestaurantOpenHours
        fields = ['mon_open', 'mon_close', 'tue_open', 'tue_close', 'wed_open',
                  'wed_close', 'thu_open', 'thu_close', 'fri_open', 'fri_close', 'sat_open',
                  'sat_close', 'sun_open', 'sun_close']
        read_only_fields = ['restaurant']

    

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


class MenuItemSerializer(serializers.ModelSerializer):
    #restaurant -- not explicit at creation
    item_name = serializers.CharField(max_length=100)
    
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    #calories -- implicit
    
    """Note to reconsider if we need these tags"""
    food_type_tag = serializers.PrimaryKeyRelatedField(queryset=models.FoodTypeTag.objects.all())
    taste_tags = serializers.PrimaryKeyRelatedField(queryset=models.TasteTag.objects.all(), many=True)
    cook_style_tags = serializers.PrimaryKeyRelatedField(queryset=models.CookStyleTag.objects.all())
    
    time_of_day_available = serializers.ChoiceField(choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Anytime', 'Anytime'),
    ])
    specialty_item = serializers.BooleanField(default=False)

    class Meta:
        model = models.MenuItem
        fields = ['id','item_name', 'average_rating', 'price', 'calories', 'food_type_tags', 
                  'taste_tags', 'cook_style_tags', 'time_of_day_available', 'specialty_item']
        read_only_fields = ['restaurant']
