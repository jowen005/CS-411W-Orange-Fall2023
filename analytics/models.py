from django.db import models
from restaurants.models import MenuItem
from patron.models import Patron
from django.contrib.auth import get_user_model

User = get_user_model()

from django.db import models

class GlobalAnalytics(models.Model):
    number_of_males = models.IntegerField()
    number_of_females = models.IntegerField()
    number_of_other = models.IntegerField()
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

    def __str__(self):
        return f"Global Analytics - {self.id}"


    class Meta:
        db_table = 'Global_Analytics'
