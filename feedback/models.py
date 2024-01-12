from django.db import models
from restaurants.models import MenuItem
from django.contrib.auth import get_user_model


User = get_user_model()


class Reviews(models.Model):
    #When patron delete his account, the reviews still remains.
    #when menu_item deleted, the reviews will not available.
    #when menuItem_history deleted, the reviews still remains.
    patron = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patron_name = models.CharField(max_length=255,null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)
    
    review = models.CharField(max_length=255,null=True)
    rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
    )
    review_datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.review_datetime.strftime('%d/%m/%y %H:%M:%S')
    
    
    def save(self, *args, **kwargs):
        #get patron name
        from patron.models import Patron
        patron_profile = Patron.objects.get(user=self.patron)
        self.patron_name = patron_profile.name
        super().save(*args, **kwargs)  # Call the parent class's save method

        # Calculate the new average rating for the associated menu item
        menu_item = self.menu_item
        reviews = Reviews.objects.filter(menu_item=menu_item)
        total_ratings = sum(float(r.rating) for r in reviews)
        average_rating = total_ratings / len(reviews)

        # Update the average_rating field in the MenuItem model
        menu_item.average_rating = average_rating
        menu_item.save()
    
    class Meta:
        db_table = 'Reviews'

class AppSatisfaction(models.Model):
        # When patron or restaurant user deletes their account the review still remains
        user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

        review = models.CharField(max_length=255,null=True)
        
        rating = models.DecimalField(
        max_digits=8,  # Total number of digits
        decimal_places=2,  # Maximum of 2 decimal places
        default=0.0
        )

        review_datetime = models.DateTimeField(auto_now_add=True)

        def formatted_datetime(self):
            return self.review_datetime.strftime('%d/%m/%y %H:%M:%S')
        
        class Meta:
             db_table = 'AppSatisfaction'
        
        