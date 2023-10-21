from django.contrib import admin

# Register your models here.
from .models import Patron
admin.site.register(Patron)

from .models import Bookmark
admin.site.register(Bookmark)

from .models import MenuItemHistory
admin.site.register(MenuItemHistory)

from .models import PatronSearchHistory
admin.site.register(PatronSearchHistory)
