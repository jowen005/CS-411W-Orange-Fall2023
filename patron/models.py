from django.db import models
from restaurants.models import MenuItem
from django.contrib.auth import get_user_model

User = get_user_model()

class Patron(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patron')
    name = models.CharField(max_length=255)
    dob = models.DateField()
    calorie_limit = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    price_preference = models.CharField(max_length=5, choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$')])
    zipcode = models.CharField(max_length=10)
    dietary_restriction = models.CharField(max_length=255, blank=True)
    palate_preference = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.patron_name
    
    class Meta:
        db_table = 'Patrons'


class Bookmark(models.Model):
    """A bookmarked item associated with the patron"""
    patron = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.patron.username} - {self.item_name}'

    class Meta:
        db_table = 'Bookmarks'
        unique_together = ('patron', 'menu_item') # Ensure each patron can bookmark an item only once
