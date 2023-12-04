from django.utils import timezone
from django.core.serializers import serialize
import sys

from restaurants.models import MenuItem
from analytics.models import MenuItemPerformanceAnalytics
from ..models import MenuItemPerformanceTrends
from . import trends


# (Trend Type, Analytic Attr)
TREND_TYPES = [('excluded', 'exclusion_count'), 
                ('history', 'number_of_added_to_History'),
                ('avg_rating', 'average_rating')]


def driver():
        
    items = list(MenuItem.objects.all().order_by('id'))

    analytics_set = MenuItemPerformanceAnalytics.objects.all()
    current_datestamp=timezone.now()
    objs_to_create = []

    print(f'{MenuItemPerformanceTrends.__name__}:')
    for item in items:
        item_analytics = analytics_set.filter(menuItem_id=item)

        item_data = trends.calculate(item_analytics, TREND_TYPES)

        for entry in item_data:
            entry['item'] = item
            obj = MenuItemPerformanceTrends(**entry, date_stamp=current_datestamp)
            
            print(f'{obj} | Size in Bytes: {sys.getsizeof(serialize("json", [obj]))}') #NOTE
            objs_to_create.append(obj)
    
    MenuItemPerformanceTrends.objects.bulk_create(objs_to_create)   # @500 bytes per model, ~134.2K bulk
    print(f"\tNumber Created: {len(objs_to_create)}\n")

