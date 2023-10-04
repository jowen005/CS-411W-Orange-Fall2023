from django.apps import AppConfig
from patron.models import Patron
from restaurant.models import #tags? menu items? I think I need from here

class PatronConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patron'

class SearchHandler:
    def preformQuickSearch(patron):
        #predefine all the advanced search options
        #call advanced search
        pass
    def preformAdvancedSearch(patron):
        #load patron details
        #generate SQL query.
        #send query to database.
        #return results list. 