from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Serializer for Rest Tag model
class RestTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)
    
    class Meta:
        model = models.RestTag
        fields = '__all__'


# Serializer for Restaurant model
class RestaurantListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = models.Restaurant
        fields = ['id', 'name']


class RestaurantMenuItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    price_level = serializers.ChoiceField(choices=[
        ('$','$'),
        ('$$','$$'),
        ('$$$','$$$'),
    ])

    class Meta:
        model = models.Restaurant
        fields = ['id', 'name', 'price_level']


class RestaurantGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    # tags = serializers.PrimaryKeyRelatedField(queryset=models.RestTag.objects.all(),many=True)
    tags = RestTagSerializer(many=True)
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
        read_only_fields = ['owner']


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    tags = serializers.PrimaryKeyRelatedField(queryset=models.RestTag.objects.all(),many=True)
    # tags = RestTagSerializer(many=True)
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
        read_only_fields = ['owner']


# Serializer for Food Type model
class FoodTypeTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.FoodTypeTag
        fields = '__all__'


# Serializer for Cook Style Tag model
class CookStyleTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.CookStyleTag
        fields = '__all__'


# Serializer for Taste Tag model
class TasteTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.TasteTag
        fields = '__all__'


# Serializer for Restriction Tag model
class RestrictionTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.RestrictionTag
        fields = '__all__'


# Serializer for Allergy Tag model
class AllergyTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.AllergyTag
        fields = '__all__'


# Serializer for Ingredient Tag model
class IngredientTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20)
    
    class Meta:
        model = models.IngredientTag
        fields = '__all__'


class MenuItemNameSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(max_length=100)

    class Meta:
        model = models.MenuItem
        fields = ['id', 'item_name']


# Serializer for Menu Item model
class MenuItemListSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(max_length=100)
    #calories
    restaurant = RestaurantMenuItemSerializer()
    #avg rating
    #price

    class Meta:
        model = models.MenuItem
        fields = ['id', 'item_name', 'calories', 'average_rating', 'price', 'restaurant']


class MenuItemGetSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    food_type_tag = FoodTypeTagSerializer()
    taste_tags = TasteTagSerializer(many=True)
    cook_style_tags = CookStyleTagSerializer()
    menu_restriction_tag = RestrictionTagSerializer(many=True)
    menu_allergy_tag = AllergyTagSerializer(many=True)
    ingredients_tag = IngredientTagSerializer(many=True)
    restaurant = RestaurantMenuItemSerializer()

    # food_type_tag = serializers.PrimaryKeyRelatedField(queryset=models.FoodTypeTag.objects.all())
    # taste_tags = serializers.PrimaryKeyRelatedField(queryset=models.TasteTag.objects.all(), many=True)
    # cook_style_tags = serializers.PrimaryKeyRelatedField(queryset=models.CookStyleTag.objects.all())
    # menu_restriction_tag = serializers.PrimaryKeyRelatedField(queryset=models.RestrictionTag.objects.all(), many=True)
    # menu_allergy_tag = serializers.PrimaryKeyRelatedField(queryset=models.AllergyTag.objects.all(), many=True)
    # ingredients_tag = serializers.PrimaryKeyRelatedField(queryset=models.IngredientTag.objects.all(), many=True)

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
        # read_only_fields = ['restaurant']



class MenuItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    # food_type_tag = FoodTypeTagSerializer()
    # taste_tags = TasteTagSerializer(many=True)
    # cook_style_tags = CookStyleTagSerializer()
    # menu_restriction_tag = RestrictionTagSerializer(many=True)
    # menu_allergy_tag = AllergyTagSerializer(many=True)
    # ingredients_tag = IngredientTagSerializer(many=True)

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
        read_only_fields = ['restaurant']
