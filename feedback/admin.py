from django.contrib import admin

# Register your models here.
#from .models import Ratings
#admin.site.register(Ratings)

from .models import Reviews
admin.site.register(Reviews)
