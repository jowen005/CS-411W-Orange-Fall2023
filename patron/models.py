from django.db import models
from restaurants.models import MenuItem,RestrictionTag,AllergyTag,TasteTag,IngredientTag
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from feedback.models import Reviews

User = get_user_model()

class Patron(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patron')
    name = models.CharField(max_length=255)
    dob = models.DateField()
    calorie_limit = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    price_max = models.PositiveIntegerField(null=True)
    zipcode = models.CharField(max_length=10)
    patron_restriction_tag = models.ManyToManyField(RestrictionTag)
    patron_allergy_tag = models.ManyToManyField(AllergyTag)
    disliked_ingredients = models.ManyToManyField(IngredientTag)
    patron_taste_tag = models.ManyToManyField(TasteTag)
    calorie_level = models.PositiveIntegerField(null=True)

	#Supporting information for suggestion feeds
    profile_updated = models.BooleanField(default=True)

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
            if start <= self.calorie_limit <= end:
                return level

    def save(self, *args, **kwargs):
        self.calorie_level = self.calculate_calorie_level()
        super(Patron, self).save(*args, **kwargs)

    
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
        return f'{self.patron.username} - {self.menu_item.item_name}'

    class Meta:
        db_table = 'Bookmarks'
        unique_together = ('patron', 'menu_item') # Ensure each patron can bookmark an item only once

class PatronSearchHistory(models.Model):
    """A patron search history associated with the patron"""
    patron = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'search_history')
    query = models.CharField(max_length=255) 
    calorie_limit = models.PositiveIntegerField(null=True, blank=True)

    dietary_restriction_tags = models.ManyToManyField(RestrictionTag)
    allergy_tags = models.ManyToManyField(AllergyTag)
    disliked_ingredients = models.ManyToManyField(IngredientTag)
    patron_taste_tags = models.ManyToManyField(TasteTag)
    
    # store the price range number which min to max. 
    price_min = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )
    price_max = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )

    search_datetime = models.DateTimeField(auto_now_add=True)
    
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
            if start <= self.calorie_limit <= end:
                return level

    def save(self, *args, **kwargs):
        self.calorie_level = self.calculate_calorie_level()
        super(PatronSearchHistory, self).save(*args, **kwargs)

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
        return f'{self.patron.username} - {self.menu_item.item_name}'
    
    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')

    class Meta:
        db_table = 'MenuItemHistory'

class PatronSuggestionVector(models.Model):
    """A suggestion vector associated with a patron"""
    patron = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestion_vector')
    tag_id = models.PositiveIntegerField()
    TAG_TABLES = [("FoodTag","FoodTag"), ("TasteTag","TasteTag"), ("CookTag","CookTag"), ("IngredientTag","IngredientTag")]
    tag_table = models.CharField(choices=TAG_TABLES,null=True,max_length=15)
    rating = models.DecimalField(max_digits=8, decimal_places=7) #this value must exist

    def __str__(self):
        f'{{"id":{self.id},"username":{self.patron.username},"patron_id":{self.patron.id},"tag_table":{self.tag_table},"tag_id":{self.tag_table},"rating":{self.rating}}}'

    class Meta:
        db_table = 'PatronSuggestionVector'

