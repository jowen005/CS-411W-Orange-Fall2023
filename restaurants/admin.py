from django.contrib import admin

# Register your models here.
from .models import RestTag
admin.site.register(RestTag)

from .models import Restaurant
admin.site.register(Restaurant)

from .models import RestaurantOpenHours
admin.site.register(RestaurantOpenHours)

from .models import FoodTypeTag
admin.site.register(FoodTypeTag)

from .models import CookStyleTag
admin.site.register(CookStyleTag)

from .models import TasteTag
admin.site.register(TasteTag)

from .models import MenuItem
admin.site.register(MenuItem)