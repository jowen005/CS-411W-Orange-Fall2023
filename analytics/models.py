from django.db import models
from restaurants.models import MenuItem, CookStyleTag, TasteTag,RestrictionTag, AllergyTag,IngredientTag
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models

class GlobalAnalytics(models.Model):
    total_males = models.IntegerField()
    total_females = models.IntegerField()
    total_other = models.IntegerField()
    users_18_24 = models.IntegerField()
    users_25_34 = models.IntegerField()
    users_35_44 = models.IntegerField()
    users_45_54 = models.IntegerField()
    users_55_64 = models.IntegerField()
    users_65_and_up = models.IntegerField()
    total_users = models.IntegerField()
    total_patrons = models.IntegerField()
    total_restaurants = models.IntegerField()
    total_menu_items = models.IntegerField()
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Global Analytics - {self.id}"

    class Meta:
        db_table = 'Global_Analytics'

class CalorieAnalytics(models.Model):
    LEVEL_CALORIE = [
        (0, 'Invalid'),(1, "0 - 199"), (2, '200 - 399'), (3 , '400 - 599'), 
        (4, '600 - 799'), (5, '800 - 999'), (6, '1000 - 1199'),
        (7,'1200 - 1399'),(8,'1400 - 1599'),(9, '1600 - 1799'),
        (10, '1800 - 1999'), (11, '2000 and up')
    ]
    calorie_level = models.IntegerField(choices=LEVEL_CALORIE,default=0,null=True)
    number_of_profiles = models.PositiveIntegerField()
    number_of_menuItems = models.PositiveIntegerField()
    number_of_searches = models.PositiveIntegerField()
    number_of_items_added_HIS = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Calorie_Analytics - {self.id}"
    class Meta:
        db_table = 'Calorie_Analytics'

class RestrictionTagAnalytics(models.Model):
    tag_id = models.ForeignKey(RestrictionTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()
    number_of_HIS = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"RestrictionTagAnalytics - {self.id}"
    class Meta:
        db_table = 'RestrictionTagAnalytics'

class AllergiesTagAnalytics(models.Model):
    tag_id = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()
    number_of_HIS = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"AllergiesTagAnalytics - {self.id}"
    class Meta:
        db_table = 'AllergiesTagAnalytics'

class IngredientTagAnalytics(models.Model):
    tag_id = models.ForeignKey(IngredientTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()
    number_of_HIS = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"IngredientTagAnalytics - {self.id}"
    class Meta:
        db_table = 'IngredientTagAnalytics'

class TasteTagAnalytics(models.Model):
    tag_id = models.ForeignKey(TasteTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()
    number_of_HIS = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"TasteTagAnalytics - {self.id}"
    class Meta:
        db_table = 'TasteTagAnalytics'

class CookStyleAnalytics(models.Model):
    tag_id = models.ForeignKey(CookStyleTag, on_delete=models.CASCADE)
    number_of_menuItem = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()
    number_of_HIS = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"CookStyleAnalytics - {self.id}"
    class Meta:
        db_table = 'CookStyleAnalytics'

class MenuItemPerformanceAnalytics(models.Model):
    menuItem_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    #number_of_search_exclued = models.PositiveIntegerField()
    number_of_added_to_bookmark = models.PositiveIntegerField()
    number_of_added_to_History = models.PositiveIntegerField()
    number_of_ratings = models.PositiveIntegerField()
    average_rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"MenuItemPerformanceAnalytics - {self.id}"
    
    class Meta:
        db_table = 'MenuItemPerformanceAnalytics'

class AppSatisfactionAnalytics(models.Model):
    average_rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )
    number_of_rating_total = models.PositiveIntegerField()
    number_of_rating_since = models.PositiveIntegerField() #TODO Remove

    def __str__(self):
        return f"AppSatisfactionAnalytics - {self.id}"
    
    class Meta:
        db_table = 'AppSatisfactionAnalytics'