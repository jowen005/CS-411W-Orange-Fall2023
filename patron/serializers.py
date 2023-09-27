from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from restaurants.models import MenuItem,Restriction_tag,Allergy_tag,TasteTag
from django.core.validators import MinValueValidator, MaxValueValidator
#from ..restaurants import serializers


User = get_user_model()

# Serializer for Patron model
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
        fields = '__all__'
        # fields = ['id', 'user', 'name', 'dob', 'calorie_limit', 'gender', 'price_preference', 'zipcode', 'dietary_restriction',
        #           'palate_allergy_tag', 'patron_taste_tag', 'patron_restriction_tag']
        read_only_fields = ['user']

# Serializer for Bookmark model
class BookmarkSerializer(serializers.ModelSerializer):
    # Not in the same app
    #menu_item = MenuItemSerializer(many=False)
    #Next line might cause same problems as it did in the owner line in Restaurant serializer
    #patron = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    bookmarked_datetime = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = models.Bookmark
        fields = '__all__'
        #fields = ['id', 'menu_item', 'bookmarked_datetime']
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

# Serializer for Patron Search History model    
class PatronSearchHistorySerializer(serializers.ModelSerializer):
    # If not working uncomment patron
    #patron = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    query = serializers.CharField(max_length=255)
    #calorie_limit = serializers.IntegerField(null=True, blank=True)
    dietary_restriction = serializers.CharField(max_length=255, blank=True)
    price_min = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0.01)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )
    price_max = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0.01)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )
    search_datetime = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = models.PatronSearchHistory
        fields = '__all__'
        read_only_fiels = ['patron']


    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

# Serializer for Meal History model    
class MealHistorySerializer(serializers.ModelSerializer):
    #patron = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    mealHS_datetime = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = models.MealHistory
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')



 