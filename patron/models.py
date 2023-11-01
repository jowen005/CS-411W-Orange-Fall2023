from django.db import models
from restaurants.models import MenuItem,RestrictionTag,AllergyTag,TasteTag,IngredientTag
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from feedback.models import Reviews

User = get_user_model()

class Patron(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patron')
    name = models.CharField(max_length=255)
    dob = models.DateField()
    calorie_limit = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    # price_preference = models.CharField(max_length=5, choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$')])
    price_max = models.PositiveIntegerField(null=True)

    zipcode = models.CharField(max_length=10)
    patron_restriction_tag = models.ManyToManyField(RestrictionTag)
    patron_allergy_tag = models.ManyToManyField(AllergyTag)
    disliked_ingredients = models.ManyToManyField(IngredientTag)
    patron_taste_tag = models.ManyToManyField(TasteTag)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'PatronProfiles'


class Bookmark(models.Model):
    """A bookmarked item associated with the patron"""
    patron = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True) 
    bookmarked_datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')


    def __str__(self):
        return f'{self.patron.username} - {self.item_name}'

    class Meta:
        db_table = 'Bookmarks'
        unique_together = ('patron', 'menu_item') # Ensure each patron can bookmark an item only once

class PatronSearchHistory(models.Model):
    """A patron search history associated with the patron"""
    patron = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'search_history')
    query = models.CharField(max_length=255) 
    calorie_limit = models.PositiveIntegerField(null=True, blank=True)

    #Replace this
    # dietary_restriction = models.CharField(max_length=255, blank=True)

    #With this
    dietary_restriction_tags = models.ManyToManyField(RestrictionTag)
    allergy_tags = models.ManyToManyField(AllergyTag)
    disliked_ingredients = models.ManyToManyField(IngredientTag)
    patron_taste_tags = models.ManyToManyField(TasteTag)

    #conversion from price level to price min max
    # QS - in backend
    # AS - in frontend
    
    # store the price range number which min to max. 
    price_min = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0.01)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )
    price_max = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0.01)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )
    search_datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

    class Meta:
        db_table = 'PatronSearchHistory'

class MenuItemHistory(models.Model):
    """A MenuItem history associated with a menu item"""
    patron = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_history')
    
    review = models.OneToOneField(Reviews, on_delete=models.SET_NULL, null=True)
    
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)  
    MenuItemHS_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patron.username} - {self.menu_item}'
    
    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

    class Meta:
        db_table = 'MenuItemHistory'
