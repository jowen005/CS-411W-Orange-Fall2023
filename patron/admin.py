from django.contrib import admin
from .models import Patron, Bookmark, MenuItemHistory, PatronSearchHistory

# Register your models here.
admin.site.register(Patron)
admin.site.register(Bookmark)
admin.site.register(MenuItemHistory)
admin.site.register(PatronSearchHistory)

