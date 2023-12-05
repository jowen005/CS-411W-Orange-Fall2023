from django.db import models
from abc import ABC

from django.contrib.auth import get_user_model
from restaurants.models import (RestrictionTag, AllergyTag, TasteTag, 
                                IngredientTag, CookStyleTag, MenuItem)

User = get_user_model()


class TrendsMixin(models.Model):
    TREND_TYPES = []

    trend_type = models.CharField(choices=TREND_TYPES, max_length=20, null=True)
    coeff0 = models.FloatField(null=True)
    coeff1 = models.FloatField(null=True)
    coeff2 = models.FloatField(null=True)
    coeff3 = models.FloatField(null=True)
    coeff4 = models.FloatField(null=True)
    coeff5 = models.FloatField(null=True)
    # behavior = models.FloatField(null=True)
    x_min = models.DateTimeField(null=True)
    x_max = models.DateTimeField(null=True)
    y_min = models.IntegerField(null=True)
    y_max = models.IntegerField(null=True)
    date_stamp = models.DateTimeField(null=True)

    class Meta:
        abstract = True


# (num_cal_levels * num_trend_types) per datestamp
class CalorieTrends(TrendsMixin):
    TREND_TYPES = [('search', 'search'), ('history', 'history')]
    LEVEL_CALORIE = [
        (0, 'Invalid'),(1, "0 - 199"), (2, '200 - 399'), (3 , '400 - 599'), 
        (4, '600 - 799'), (5, '800 - 999'), (6, '1000 - 1199'),
        (7,'1200 - 1399'),(8,'1400 - 1599'),(9, '1600 - 1799'),
        (10, '1800 - 1999'), (11, '2000 and up')
    ]
    calorie_level = models.IntegerField(choices=LEVEL_CALORIE,default=0,null=True)

    def __str__(self):
        return f"{self.date_stamp} | CalorieTrends - {self.id} | Calorie Level: {self.calorie_level}"

    class Meta:
        db_table = 'CalorieTrends'
    

# (num_tags * num_trend_types) per datestamp
class RestrictionTagTrends(TrendsMixin):
    TREND_TYPES = [('search', 'search'), ('history', 'history')]
    tag = models.ForeignKey(RestrictionTag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_stamp} | RestrictionTagTrends - {self.id} | Tag ID: {self.tag.id}"

    class Meta:
        db_table = 'RestrictionTagTrends'


# (num_tags * num_trend_types) per datestamp
class AllergyTagTrends(TrendsMixin):
    TREND_TYPES = [('search', 'search'), ('history', 'history')]
    tag = models.ForeignKey(AllergyTag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_stamp} | AllergyTagTrends - {self.id} | Tag ID: {self.tag.id}"

    class Meta:
        db_table = 'AllergyTagTrends'


# (num_tags * num_trend_types) per datestamp
class IngredientTagTrends(TrendsMixin):
    TREND_TYPES = [('search', 'search'), ('history', 'history')]
    tag = models.ForeignKey(IngredientTag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_stamp} | IngredientTagTrends - {self.id} | Tag ID: {self.tag.id}"

    class Meta:
        db_table = 'IngredientTagTrends'
    

# (num_tags * num_trend_types) per datestamp
class TasteTagTrends(TrendsMixin):
    TREND_TYPES = [('search', 'search'), ('history', 'history')]
    tag = models.ForeignKey(TasteTag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_stamp} | TasteTagTrends - {self.id} | Tag ID: {self.tag.id}"

    class Meta:
        db_table = 'TasteTagTrends'


# (num_tags * num_trend_types) per datestamp
class CookStyleTagTrends(TrendsMixin):
    TREND_TYPES = [('search', 'search'), ('history', 'history')]
    tag = models.ForeignKey(CookStyleTag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_stamp} | CookStyleTagTrends - {self.id} | Tag ID: {self.tag.id}"

    class Meta:
        db_table = 'CookStyleTagTrends'


# (num_menu_items * num_trend_types) per datestamp
class MenuItemPerformanceTrends(TrendsMixin):
    TREND_TYPES = [('excluded', 'excluded'), ('history', 'history'), ('avg_rating', 'avg_rating')]
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_stamp} | MenuItemPerformanceTrends - {self.id} | Item ID: {self.item.id}"

    class Meta:
        db_table = 'MenuItemPerformanceTrends'


# (num_trend_types) per datestamp
class AppSatisfactionTrends(TrendsMixin):
    TREND_TYPES = [('num_ratings', 'num_ratings'), ('avg_rating', 'avg_rating')]

    def __str__(self):
        return f"{self.date_stamp} | AppSatisfactionTrends - {self.id}"

    class Meta:
        db_table = 'AppSatisfactionTrends'

