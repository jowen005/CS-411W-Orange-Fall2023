from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
import restaurants.serializers as rs
import restaurants.models as rm
import feedback.serializers as fs
import feedback.models as fm
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class PatronGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    gender = serializers.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    zipcode = serializers.CharField(max_length=10)

    patron_restriction_tag = rs.RestrictionTagSerializer(many=True)
    patron_allergy_tag = rs.AllergyTagSerializer(many=True)
    patron_taste_tag = rs.TasteTagSerializer(many=True)
    disliked_ingredients = rs.IngredientTagSerializer(many=True)

    # patron_restriction_tag = serializers.PrimaryKeyRelatedField(queryset=rm.RestrictionTag.objects.all(), many=True)
    # patron_allergy_tag = serializers.PrimaryKeyRelatedField(queryset=rm.AllergyTag.objects.all(), many=True)
    # patron_taste_tag = serializers.PrimaryKeyRelatedField(queryset=rm.TasteTag.objects.all(), many=True)
    # disliked_ingredients = serializers.PrimaryKeyRelatedField(queryset=rm.IngredientTag.objects.all(), many=True)

    class Meta:
        model = models.Patron
        fields = '__all__'
        read_only_fields = ['user']


class PatronSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    gender = serializers.CharField(max_length=10)
    zipcode = serializers.CharField(max_length=10)

    # patron_restriction_tag = rs.RestrictionTagSerializer(many=True)
    # patron_allergy_tag = rs.AllergyTagSerializer(many=True)
    # patron_taste_tag = rs.TasteTagSerializer(many=True)
    # disliked_ingredients = rs.IngredientTagSerializer(many=True)

    patron_restriction_tag = serializers.PrimaryKeyRelatedField(queryset=rm.RestrictionTag.objects.all(), many=True)
    patron_allergy_tag = serializers.PrimaryKeyRelatedField(queryset=rm.AllergyTag.objects.all(), many=True)
    patron_taste_tag = serializers.PrimaryKeyRelatedField(queryset=rm.TasteTag.objects.all(), many=True)
    disliked_ingredients = serializers.PrimaryKeyRelatedField(queryset=rm.IngredientTag.objects.all(), many=True)

    class Meta:
        model = models.Patron
        fields = '__all__'
        read_only_fields = ['user']

 
class PatronSearchHistoryGetSerializer(serializers.ModelSerializer):
    query = serializers.CharField(max_length=255)
    calorie_limit = serializers.IntegerField()

    dietary_restriction_tags = rs.RestrictionTagSerializer(many=True)
    allergy_tags = rs.AllergyTagSerializer(many=True)
    patron_taste_tags = rs.TasteTagSerializer(many=True)
    disliked_ingredients = rs.IngredientTagSerializer(many=True)

    # dietary_restriction_tags = serializers.PrimaryKeyRelatedField(queryset=rm.RestrictionTag.objects.all(), many=True)
    # allergy_tags = serializers.PrimaryKeyRelatedField(queryset=rm.AllergyTag.objects.all(), many=True)
    # patron_taste_tags = serializers.PrimaryKeyRelatedField(queryset=rm.TasteTag.objects.all(), many=True)
    # disliked_ingredients = serializers.PrimaryKeyRelatedField(queryset=rm.IngredientTag.objects.all(), many=True)
    
    price_min = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0)],  # Positive only
    )
    price_max = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0)],  # Positive only
    )

    class Meta:
        model = models.PatronSearchHistory
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')


class PatronSearchHistorySerializer(serializers.ModelSerializer):
    query = serializers.CharField(max_length=255)
    calorie_limit = serializers.IntegerField()

    # dietary_restriction_tags = rs.RestrictionTagSerializer(many=True)
    # allergy_tags = rs.AllergyTagSerializer(many=True)
    # patron_taste_tags = rs.TasteTagSerializer(many=True)
    # disliked_ingredients = rs.IngredientTagSerializer(many=True)

    dietary_restriction_tags = serializers.PrimaryKeyRelatedField(queryset=rm.RestrictionTag.objects.all(), many=True)
    allergy_tags = serializers.PrimaryKeyRelatedField(queryset=rm.AllergyTag.objects.all(), many=True)
    patron_taste_tags = serializers.PrimaryKeyRelatedField(queryset=rm.TasteTag.objects.all(), many=True)
    disliked_ingredients = serializers.PrimaryKeyRelatedField(queryset=rm.IngredientTag.objects.all(), many=True)
    
    price_min = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0)],  # Positive only
    )
    price_max = serializers.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0)],  # Positive only
    )

    class Meta:
        model = models.PatronSearchHistory
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')


class BookmarkGetSerializer(serializers.ModelSerializer):
    menu_item = rs.MenuItemListSerializer()
    # menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())

    class Meta:
        model = models.Bookmark
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')


class BookmarkSerializer(serializers.ModelSerializer):
    # menu_item = rs.MenuItemListSerializer()
    menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())

    class Meta:
        model = models.Bookmark
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')


class MenuItemHistoryGetSerializer(serializers.ModelSerializer):
    menu_item = rs.MenuItemListSerializer()
    review = fs.ReviewsSerializer()
    # review = fs.ReviewsGetSerializer()
    # menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())

    class Meta:
        model = models.MenuItemHistory
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')


   
class MenuItemHistorySerializer(serializers.ModelSerializer):
    # menu_item = rs.MenuItemListSerializer()
    menu_item = serializers.PrimaryKeyRelatedField(queryset=rm.MenuItem.objects.all())
    review = serializers.PrimaryKeyRelatedField(queryset=fm.Reviews.objects.all())

    class Meta:
        model = models.MenuItemHistory
        fields = '__all__'
        read_only_fields = ['patron']

    # def formatted_datetime(self):
    #     return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')
