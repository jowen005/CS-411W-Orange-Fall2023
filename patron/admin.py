from django.contrib import admin
import models as pm

# Register your models here.
admin.site.register(pm.Patron)
admin.site.register(pm.Bookmark)
admin.site.register(pm.MenuItemHistory)
admin.site.register(pm.PatronSearchHistory)

