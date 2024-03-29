from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
import math

#from accounts.utils.vectorize import vectorizeMenuItem

User = get_user_model()

# Create your models here.
class RestTag(models.Model):
    """
        A descriptive tag that describes the type of restaurant or cuisine
        Examples: Fast food, Thai, Chinese, Mexican, Bar, 
    """
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'RestTags'


class Restaurant(models.Model):
    """A restaurant"""
    #General Info
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    tags = models.ManyToManyField(RestTag)
    price_level = models.CharField(max_length=3, choices=[
        ('$','$'),
        ('$$','$$'),
        ('$$$','$$$'),
    ])
    phone_number = models.CharField(max_length=12)  #Change later to phone number field (google)
    website = models.URLField()

    street_name = models.CharField(max_length=50)   #Might be a google library for addresses
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=9)       #Might want to extend to 9 digits
    mon_open = models.TimeField(null=True)
    mon_close = models.TimeField(null=True)
    tue_open = models.TimeField(null=True)
    tue_close = models.TimeField(null=True)
    wed_open = models.TimeField(null=True)
    wed_close = models.TimeField(null=True)
    thu_open = models.TimeField(null=True)
    thu_close = models.TimeField(null=True)
    fri_open = models.TimeField(null=True)
    fri_close = models.TimeField(null=True)
    sat_open = models.TimeField(null=True)
    sat_close = models.TimeField(null=True)
    sun_open = models.TimeField(null=True)
    sun_close = models.TimeField(null=True)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Restaurants'


# Appetizer, Main Course, Dessert Beverage
class FoodTypeTag(models.Model):
    """A tag representing the type of food the menu item is"""
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "FoodTypeTags"


# Baked, Grilled, Fried
class CookStyleTag(models.Model):
    """A tag representing how the menu item is cooked"""
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "CookStyleTags"


# Tags for taste (spicy, salty, smoked, etc.)
class TasteTag(models.Model):
    """A tag representing the taste of a menu item"""
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'TasteTags'


# Tags for Restriction(halal,veg.)
class RestrictionTag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'RestrictionTag'


# Tags for Allergy (Nuts)
class AllergyTag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'AllergyTags'


#Tags for ingredients (Beef)
class IngredientTag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'IngredientTags'


# Define the model for menu items
class MenuItem(models.Model):
    
    # Item information
    item_name = models.CharField(max_length=100)

    # Foreign Key to the restaurant that offers this menu item
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_items')

    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    number_of_rating = models.PositiveIntegerField(default=0)
    
    price = models.DecimalField(max_digits=6, decimal_places=2)
    calories = models.PositiveIntegerField()

    food_type_tag = models.ForeignKey(FoodTypeTag, on_delete=models.SET_NULL, null=True)
    taste_tags = models.ManyToManyField(TasteTag)
    cook_style_tags = models.ForeignKey(CookStyleTag, on_delete=models.SET_NULL, null=True)
    menu_restriction_tag = models.ManyToManyField(RestrictionTag)
    menu_allergy_tag = models.ManyToManyField(AllergyTag)
    ingredients_tag = models.ManyToManyField(IngredientTag)

    #Supporting information for suggestion feeds
    suggestion_vector = models.CharField(max_length=128,null=True)
    inverse_sqrt = models.DecimalField(max_digits=10, decimal_places=8, default=1)
    
    time_of_day_available = models.CharField(max_length=20, choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Anytime', 'Anytime'),
    ])

    is_modifiable = models.BooleanField(default=False)
   
    calorie_level = models.PositiveIntegerField(null=True)
    CALORIE_LEVEL_RANGES = [
        (0, 199, 1),
        (200, 399, 2),
        (400, 599, 3),
        (600,799,4),
        (800,999,5),
        (1000,1199,6),
        (1200,1399,7),
        (1400,1599,8),
        (1600,1799,9),
        (1800, 1999, 10),
        (2000, float('inf'), 11),
    ]

    def calculate_calorie_level(self):
        for start, end, level in self.CALORIE_LEVEL_RANGES:
            if start <= self.calories <= end:
                return level

    def save(self, *args, **kwargs):
        self.calorie_level = self.calculate_calorie_level()
        #self.vectorizeMenuItem()
        # self.prep_for_vector()
        super(MenuItem, self).save(*args, **kwargs)
        self.vectorizeMenuItem()

    def __str__(self):
        return self.item_name 

    # def prep_for_vector(self):
    #     tag_counts = {TagModel.__name__:TagModel.objects.all().count() for TagModel in self.TAGS_TO_TRACK}
    #     vectorizeMenuItem(self, tag_counts)

    class Meta:
        db_table = 'MenuItems'

    TAGS_TO_TRACK = [FoodTypeTag, TasteTag, CookStyleTag, IngredientTag]

    def vectorizeMenuItem(self):
        # print('Im vectorizing')
        tag_counts = {TagModel.__name__:TagModel.objects.all().count() for TagModel in self.TAGS_TO_TRACK}
        Item = self
        FoodTagCount = tag_counts['FoodTypeTag']
        TasteTagCount = tag_counts['TasteTag']
        CookTagCount = tag_counts['CookStyleTag']
        IngredientTagCount = tag_counts['IngredientTag']
        
        TotalTags = FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount

        FoodList = ['0'] * FoodTagCount
        TasteList = ['0'] * TasteTagCount
        CookList = ['0'] * CookTagCount
        IngredientList = ['0'] * IngredientTagCount
        
        selected_tags = 2
        FoodList[Item.food_type_tag.id-1] = '1'    
        CookList[Item.cook_style_tags.id-1] = '1'
        
        for Tag in Item.taste_tags.values_list("id",flat=True):
            TasteList[Tag-1] = '1'
            selected_tags += 1

        for Tag in Item.ingredients_tag.values_list("id",flat=True):
            IngredientList[Tag-1] = '1'
            selected_tags += 1

        #Maybe I should make this a json with tag names?
        #print(FoodList)
        FoodString = "".join(FoodList)
        TasteString = "".join(TasteList)
        CookString = "".join(CookList)
        IngrString = "".join(IngredientList)
        FinalVectorString = FoodString + ';' + TasteString + ';' + CookString + ';' + IngrString + ';'
        Item.suggestion_vector = FinalVectorString
        # print(FinalVectorString)
        #compute and save normalizing value
        Item.inverse_sqrt = 1/math.sqrt(selected_tags)
        super(MenuItem, self).save()
    
