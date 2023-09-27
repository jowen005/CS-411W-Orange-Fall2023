from django.db import models
from restaurants.models import MenuItem
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()

class Reviews(models.Model):
    #When patron delete his account, the reviews still remains.
    #when menu_item deleted, the reviews will not available.
    patron = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True) 
    patron_review = models.CharField(max_length=255,null=True)
    review_datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')
    
    class Meta:
        db_table = 'Reviews'

class Ratings(models.Model):
    patron = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True) 
    ratings = models.IntegerField(
        choices = [('1', '1'), ('2', '2'), ('3', '3'),('4', '4'),('5', '5')],
    )
    rating_datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.rating_datetime.strftime('%d/%m/%y %H:%M:%S')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the parent class's save method

        # Calculate the new average rating for the associated menu item
        menu_item = self.menu_item
        ratings = Ratings.objects.filter(menu_item=menu_item)
        total_ratings = sum(float(r.ratings) for r in ratings)
        average_rating = total_ratings / len(ratings)

        # Update the average_rating field in the MenuItem model
        menu_item.average_rating = average_rating
        menu_item.save()

    class Meta:
        db_table = 'Ratings'

