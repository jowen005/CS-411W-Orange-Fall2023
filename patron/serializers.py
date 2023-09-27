from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from restaurants.models import MenuItem,Restriction_tag,Allergy_tag,TasteTag
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
    patron_restriction_tag = serializers.PrimaryKeyRelatedField(Restriction_tag)
    patron_allergy_tag = serializers.PrimaryKeyRelatedField(Allergy_tag)
    patron_taste_tag = serializers.PrimaryKeyRelatedField(TasteTag)

    class Meta:
        model = models.Patron
        fields = '_all_'
        # fields = ['id', 'user', 'name', 'dob', 'calorie_limit', 'gender', 'price_preference', 'zipcode', 'dietary_restriction',
        #           'palate_allergy_tag', 'patron_taste_tag', 'patron_restriction_tag']
        read_only_fields = ['user']

class BookmarkSerializer(serializers.ModelSerializer):
    # Not in the same app
    #menu_item = MenuItemSerializer(many=False)
    #Figured that next line would cause same problems as it did in the owner line in Restaurant serializer
    #patron = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    bookmarked_datetime = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = models.Bookmark
        fields = '_all_'
        #fields = ['id', 'menu_item', 'bookmarked_datetime']
        read_only_fields = ['patron']

    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')
    
# class PatronSearchHistorySerializer(serializers.ModelSerializer):

#     query = serializers.CharField(max_length=255)

 