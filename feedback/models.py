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
    restaurant_replies = models.CharField(max_length=255,null=True)
    review_datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.search_datetime.strftime('%d/%m/%y %H:%M:%S')
    
    class Meta:
        db_table = 'Reviews'

class Ratings(models.Model):
    patron = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True) 
    ratings = models.DecimalField(
        max_digits=2,  # Total number of digits
        decimal_places=1,  # Maximum of 2 decimal places
        validators=[MinValueValidator(0.1)],  # Positive only
        null=True,  # Allow null values
        blank=True
    )
    class Meta:
        db_table = 'Ratings'
