from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Restaurant)
admin.site.register(models.RestaurantOpenHours)
admin.site.register(models.RestTag)