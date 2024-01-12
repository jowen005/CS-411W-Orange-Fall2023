from django.contrib import admin
import models as rm

admin.site.register(rm.RestTag)
admin.site.register(rm.Restaurant)
admin.site.register(rm.FoodTypeTag)
admin.site.register(rm.CookStyleTag)
admin.site.register(rm.TasteTag)
admin.site.register(rm.RestrictionTag)
admin.site.register(rm.AllergyTag)
admin.site.register(rm.IngredientTag)
admin.site.register(rm.MenuItem)

