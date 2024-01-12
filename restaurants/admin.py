from django.contrib import admin
from .models import (
    RestTag, Restaurant, FoodTypeTag, CookStyleTag, TasteTag,
    RestrictionTag, AllergyTag, IngredientTag, MenuItem
)

admin.site.register(RestTag)
admin.site.register(Restaurant)
admin.site.register(FoodTypeTag)
admin.site.register(CookStyleTag)
admin.site.register(TasteTag)
admin.site.register(RestrictionTag)
admin.site.register(AllergyTag)
admin.site.register(IngredientTag)
admin.site.register(MenuItem)

