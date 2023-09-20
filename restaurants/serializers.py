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
                'phone_number','street_name','city','state','zip_code']
        read_only_fields = ['owner',]


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
