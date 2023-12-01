from django.db import models
from restaurants.models import MenuItem, CookStyleTag, TasteTag, RestrictionTag, AllergyTag, IngredientTag
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
        return f"{self.date_stamp} | Global Analytics - {self.id}"

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
    number_of_searches = models.PositiveIntegerField()          #For Trend Use Only
    number_of_items_added_HIS = models.PositiveIntegerField()   #For Trend Use Only
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | Calorie Analytics - {self.id} | Level {self.calorie_level}"
    class Meta:
        db_table = 'Calorie_Analytics'


class RestrictionTagAnalytics(models.Model):
    tag_id = models.ForeignKey(RestrictionTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    exclusion_count = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()    #For Trend Use Only
    number_of_HIS = models.PositiveIntegerField()       #For Trend Use Only
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | RestrictionTagAnalytics - {self.id} | Tag: {self.tag_id}"
    class Meta:
        db_table = 'RestrictionTagAnalytics'


class AllergiesTagAnalytics(models.Model):
    tag_id = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    exclusion_count = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()    #For Trend Use Only
    number_of_HIS = models.PositiveIntegerField()       #For Trend Use Only
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | AllergiesTagAnalytics - {self.id} | Tag: {self.tag_id}"
    class Meta:
        db_table = 'AllergiesTagAnalytics'


class IngredientTagAnalytics(models.Model):
    tag_id = models.ForeignKey(IngredientTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    exclusion_count = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()    #For Trend Use Only
    number_of_HIS = models.PositiveIntegerField()       #For Trend Use Only
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | IngredientTagAnalytics - {self.id} | Tag: {self.tag_id}"
    class Meta:
        db_table = 'IngredientTagAnalytics'


class TasteTagAnalytics(models.Model):
    tag_id = models.ForeignKey(TasteTag, on_delete=models.CASCADE)
    number_of_patronProfile = models.PositiveIntegerField()
    number_of_menuItem = models.PositiveIntegerField()
    exclusion_count = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()    #For Trend Use Only
    number_of_HIS = models.PositiveIntegerField()       #For Trend Use Only
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | TasteTagAnalytics - {self.id} | Tag: {self.tag_id}"
    class Meta:
        db_table = 'TasteTagAnalytics'


class CookStyleAnalytics(models.Model):
    tag_id = models.ForeignKey(CookStyleTag, on_delete=models.CASCADE)
    number_of_menuItem = models.PositiveIntegerField()
    number_of_search = models.PositiveIntegerField()    #For Trend Use Only
    number_of_HIS = models.PositiveIntegerField()       #For Trend Use Only
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | CookStyleAnalytics - {self.id} | Tag: {self.tag_id}"
    class Meta:
        db_table = 'CookStyleAnalytics'


# class OverallFilterAnalytics(models.Model):
#     FILTER_TYPES = [('calories', 'calories'),
#                     ('cookstyletag', 'cookstyletag'),
#                     ('allergytag', 'allergytag'), 
#                     ('ingredienttag', 'ingredienttag'), 
#                     ('restrictiontag', 'restrictiontag'),
#                     ('tastetag', 'tastetag')]
    
#     filter_type = models.IntegerField(choices=FILTER_TYPES)
#     top_3_inclusions = models.JSONField()
#     top_3_added = models.JSONField()
#     top_3_exclusions = models.JSONField(null=True)
    


class MenuItemPerformanceAnalytics(models.Model):
    menuItem_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    number_of_added_to_History = models.PositiveIntegerField()  #For Trend Use Only

    exclusion_count = models.IntegerField
    top_3_allergy = models.JSONField()
    top_3_ingredients = models.JSONField()
    top_3_restrictions = models.JSONField()
    top_3_taste = models.JSONField()

    number_of_ratings = models.PositiveIntegerField()
    average_rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )
    # date_stamp = models.DateTimeField(auto_now_add = True)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.date_stamp} | MenuItemPerformanceAnalytics - {self.id} | Menu Item: {self.menuItem_id}"
    
    class Meta:
        db_table = 'MenuItemPerformanceAnalytics'


class AppSatisfactionAnalytics(models.Model):
    average_rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
    )
    number_of_rating_total = models.PositiveIntegerField()
    date_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_stamp} | AppSatisfactionAnalytics - {self.id}"
    
    class Meta:
        db_table = 'AppSatisfactionAnalytics'


# INTERMEDIATE TABLES


class OverallExclusionRecord(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    exclusion_count = models.PositiveIntegerField(default=0)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.menu_item.id} --> {self.exclusion_count}"
    
    class Meta:
        db_table = 'OverallExclusionRecord'
    

class AllergyTagExclusionRecord(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    tag = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)
    exclusion_count = models.PositiveIntegerField(default=0)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.menu_item.id}: {self.tag.title} --> {self.exclusion_count}"
    
    class Meta:
        db_table = 'AllergyTagExclusionRecord'
    

class IngredientTagExclusionRecord(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    tag = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)
    exclusion_count = models.PositiveIntegerField(default=0)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.menu_item.id}: {self.tag.title} --> {self.exclusion_count}"
    
    class Meta:
        db_table = 'IngredientTagExclusionRecord'


class RestrictionTagExclusionRecord(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    tag = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)
    exclusion_count = models.PositiveIntegerField(default=0)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.menu_item.id}: {self.tag.title} --> {self.exclusion_count}"
    
    class Meta:
        db_table = 'RestrictionTagExclusionRecord'
    

class TasteTagExclusionRecord(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    tag = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)
    exclusion_count = models.PositiveIntegerField(default=0)
    date_stamp = models.DateTimeField()

    def __str__(self):
        return f"{self.menu_item.id}: {self.tag.title} --> {self.exclusion_count}"
    
    class Meta:
        db_table = 'TasteTagExclusionRecord'