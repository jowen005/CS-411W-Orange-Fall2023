from datetime import datetime, timedelta
from django.utils import timezone

import restaurants.models as rm
import patron.models as pm
from ..models import LocalRestaurantAnalytics
from ..models import (AllergyTagExclusionRecord, IngredientTagExclusionRecord,
                      RestrictionTagExclusionRecord, TasteTagExclusionRecord,
                      OverallExclusionRecord)

# def restaurant_analysis():

#     # Past 3 Days (Data Overlap)
#     latest_datestamp = timezone.now() - timedelta(days=3)


#     restaurants = rm.Restaurant.objects.all().order_by('id')
#     items = rm.MenuItem.objects.all().order_by('id')
#     history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)

#     # Total restauratns added to history
#     for restaurant in restaurants:
#         data = {}

#         data['total']