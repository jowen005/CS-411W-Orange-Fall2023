from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
#from ..restaurants import serializers


User = get_user_model()

class PatronSerializer(serializers.ModelSerializer):
    # May be able to use writable nested serializer or the below example
    # https://stackoverflow.com/questions/42314882/drf-onetoonefield-create-serializer
    #user = serializers.PrimaryKeyRelatedField()
    name = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=10)
    price_preference = serializers.CharField(max_length=5, choices=[
        ('$', '$'), 
        ('$$', '$$'), 
        ('$$$', '$$$')])
    zipcode = serializers.CharField(max_length=10)
    dietary_restriction = serializers.CharField(max_length=255, blank=True)
    palate_preference = serializers.CharField(max_length=255, blank=True)

    class Meta:
        model = models.Patron
        fields = ['id', 'name', 'dob', 'calorie_limit', 'gender', 'price_preference', 'zipcode', 'dietary_restriction',
                  'palate_preference']
        read_only_fields = ['user']

class BookmarkSerializer(serializers.ModelSerializer):
    # Not in the same app
    #menu_item = MenuItemSerializer(many=False)
    #Figured that next line would cause same problems as it did in the owner line in Restaurant serializer
    #patron = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    menu_item = serializers.PrimaryKeyRelatedField(queryset=models.MenuItem.objects.all())

    class Meta:
        model = models.Bookmark
        fields = ['id', 'menu_item']
        read_only_fields = ['patron']

 