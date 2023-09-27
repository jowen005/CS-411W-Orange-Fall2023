from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

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


# class RestaurantOpenHours(models.Model):
#     """Describes the open hours of a restaurant"""
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
#     mon_open = models.TimeField()
#     mon_close = models.TimeField()
#     tue_open = models.TimeField()
#     tue_close = models.TimeField()
#     wed_open = models.TimeField()
#     wed_close = models.TimeField()
#     thu_open = models.TimeField()
#     thu_close = models.TimeField()
#     fri_open = models.TimeField()
#     fri_close = models.TimeField()
#     sat_open = models.TimeField()
#     sat_close = models.TimeField()
#     sun_open = models.TimeField()
#     sun_close = models.TimeField()

#     def __str__(self):
#         return f"{self.restaurant.name}'s Open Hours"

#     class Meta:
#         db_table = 'RestOpenHours'


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
        return self.tag_name

    class Meta:
        db_table = 'TasteTags'
# Tags for Restriction(halal,veg.)

class Restriction_tag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Restriction'

# Tags for Allergy (Nuts)
class Allergy_tag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Allergy_tag'

#Tags for ingredients (Beef)
class IngredientsTag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Ingredients'

# Define the model for menu items
class MenuItem(models.Model):
    
    # Item information
    item_name = models.CharField(max_length=100)

    # Foreign Key to the restaurant that offers this menu item
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_items')

    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    calories = models.PositiveIntegerField()

    food_type_tag = models.ForeignKey(FoodTypeTag, on_delete=models.SET_NULL, null=True)
    taste_tags = models.ManyToManyField(TasteTag)
    cook_style_tags = models.ForeignKey(CookStyleTag, on_delete=models.SET_NULL, null=True)
    menu_restriction_tag = models.ManyToManyField(Restriction_tag)
    menu_allergy_tag = models.ManyToManyField(Allergy_tag)
    ingredients_tag = models.ManyToManyField(IngredientsTag)
    
    time_of_day_available = models.CharField(max_length=20, choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Anytime', 'Anytime'),
    ])

    is_modifiable = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name

    class Meta:
        db_table = 'MenuItems'
