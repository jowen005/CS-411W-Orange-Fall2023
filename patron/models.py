from django.db import models
from django.conf import settings
from restaurants.models import MenuItem

class Patron(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patron')
    patron_name = models.CharField(max_length=255)
    bod = models.DateField()
    calorie_limit = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    price_preference = models.CharField(max_length=5, choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$')])
    zipcode = models.CharField(max_length=10)
    dietary_restriction = models.CharField(max_length=255, blank=True, null=True)
    palate_preference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.patron_name

class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    patron = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)  

    def __str__(self):
        return f'{self.patron.username} - {self.item_name}'

    class Meta:
        unique_together = ('patron', 'item') # Ensure each patron can bookmark an item only once