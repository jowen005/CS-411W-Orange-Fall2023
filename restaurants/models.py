from django.db import models


# Create your models here.
class RestTag(models.Model):
    """A descriptive tag that describes the type of restaurant or cuisine"""
    title = models.CharField(max_length=50)
    """What else goes in here, I don't think it should be a table if it only has this field and the auto
    generated primary key"""

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'RestTags'


class Restaurant(models.Model):
    """A restaurant"""
    #General Info
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    tags = models.ManyToManyField(RestTag)
    price_level = models.PositiveSmallIntegerField(choices=[
        (1,'$'),
        (2,'$$'),
        (3,'$$$'),
    ])
    phone_number = models.CharField(max_length=12)  #Change later to phone number field (google)
    website = models.URLField()

    street_name = models.CharField(max_length=50)   #Might be a google library for addresses
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)       #Might want to extend to 9 digits


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Restaurants'


class RestaurantOpenHours(models.Model):
    """Describes the open hours of a restaurant"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    mon_open = models.TimeField()
    mon_close = models.TimeField()
    tue_open = models.TimeField()
    tue_close = models.TimeField()
    wed_open = models.TimeField()
    wed_close = models.TimeField()
    thu_open = models.TimeField()
    thu_close = models.TimeField()
    fri_open = models.TimeField()
    fri_close = models.TimeField()
    sat_open = models.TimeField()
    sat_close = models.TimeField()
    sun_open = models.TimeField()
    sun_close = models.TimeField()

    def __str__(self):
        return f"{self.restaurant.name}'s Open Hours"

    class Meta:
        db_table = 'RestOpenHours'

# class RestaurantOpenHours(models.Model):
#     """Describes the open hours of a restaurant"""
#     DAY_CHOICES = [
#         (0, 'Sunday'),
#         (1, 'Monday'),
#         (2, 'Tuesday'),
#         (3, 'Wednesday'),
#         (4, 'Thursday'),
#         (5, 'Friday'),
#         (6, 'Saturday'),
#     ]

#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     day_of_week = models.IntegerField(choices=DAY_CHOICES)
#     opening_time = models.TimeField()
#     closing_time = models.TimeField()

#     def __str__(self):
#         return f"{self.restaurant.name}'s Open Hours"

#     class Meta:
#         db_table = 'RestOpenHours'
    
class MenuItem(models.Model):
    """A class for the individual menu items"""

    itemName = models.CharField(max_length=100)
    foodType = models.CharField(max_length=50)
    avgRating = models.DecimalField(max_length=2, decimal_places=1)
    price = models.DecimalField(max_length=20, decimal_places=2)

    class Meta:
        db_table = 'MenuItems'

    


