from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Serializer for Restaurant model
class RestaurantListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = models.Restaurant
        fields = ['id', 'name']


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
    zip_code = serializers.CharField(max_length=9)

    class Meta:
        model = models.Restaurant
        fields = '__all__'
        # fields = ['id','owner','name','rating','tags','price_level',
        #         'phone_number','website', 'street_name','city','state','zip_code',
        #         'mon_open', 'mon_close', 'tue_open', 'tue_close', 'wed_open',
        #         'wed_closea', 'thu_open', 'thu_close', 'fri_open', 'fri_close',
        #         'sat_open','sat_close', 'sun_open', 'sun_close']
        read_only_fields = ['owner']


# Serializer for Menu Item model
class MenuItemListSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(max_length=100)

    class Meta:
        model = models.MenuItem
        fields = ['id', 'item_name']


class MenuItemSerializer(serializers.ModelSerializer):
    #restaurant -- not explicit at creation
    item_name = serializers.CharField(max_length=100)
    
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    #calories -- implicit
    
    """Note to reconsider if we need these tags"""
    food_type_tag = serializers.PrimaryKeyRelatedField(queryset=models.FoodTypeTag.objects.all())
    taste_tags = serializers.PrimaryKeyRelatedField(queryset=models.TasteTag.objects.all(), many=True)
    cook_style_tags = serializers.PrimaryKeyRelatedField(queryset=models.CookStyleTag.objects.all())
    menu_restriction_tag = serializers.PrimaryKeyRelatedField(queryset=models.RestrictionTag.objects.all(), many=True)
    menu_allergy_tag = serializers.PrimaryKeyRelatedField(queryset=models.AllergyTag.objects.all(), many=True)
    ingredients_tag = serializers.PrimaryKeyRelatedField(queryset=models.IngredientTag.objects.all(), many=True)


    time_of_day_available = serializers.ChoiceField(choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Anytime', 'Anytime'),
    ])
    is_modifiable = serializers.BooleanField(default=False)

    class Meta:
        model = models.MenuItem
        fields = '__all__'
        # fields = ['id', 'restaurant', 'item_name', 'price', 'calories', 'food_type_tag', 
        #           'taste_tags', 'cook_style_tags', 'menu_restriction_tag',
        #           'menu_allergy_tag','ingredients_tag','time_of_day_available', 'is_modifiable']
        read_only_fields = ['restaurant']


# Serializer for Rest Tag model
class RestTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    
    class Meta:
        model = models.RestTag
        fields = '__all__'
        #fields = ['id', 'title']


# Serializer for Food Type model
class FoodTypeTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.FoodTypeTag
        fields = '__all__'
        #fields = ['id', 'title']


# Serializer for Cook Style Tag model
class CookStyleTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.CookStyleTag
        fields = '__all__'
        #fields = ['id', 'title']


# Serializer for Taste Tag model
class TasteTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.TasteTag
        fields = '__all__'
        #fields = ['id', 'title']


# Serializer for Restriction Tag model
class RestrictionTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.RestrictionTag
        fields = '__all__'
        #fields = ['id', 'title']


# Serializer for Allergy Tag model
class AllergyTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.AllergyTag
        fields = '__all__'
        #fields = ['id', 'title']


# Serializer for Ingredient Tag model
class IngredientTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.IngredientTag
        fields = '__all__'
        #fields = ['id', 'title']
