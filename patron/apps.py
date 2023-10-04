from django.apps import AppConfig
from patron.models import Patron
from restaurant.models import MenuItem#tags? menu items? I think I need from here

class PatronConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patron'
    