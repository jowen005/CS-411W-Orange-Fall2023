from django.utils import timezone
from analytics.models import MenuItemPerformanceAnalytics
from ..models import MenuItemPerformanceTrends
import restaurants.models as rm
from django.core.serializers import serialize
import sys
from . import trends


# (Trend Type, Analytic Attr)
TREND_TYPES = [('excluded', 'exclusion_count'), 
                ('history', 'number_of_added_to_History'),
                ('avg_rating', 'average_rating')]


def driver():
        
    items = list(rm.MenuItem.objects.all().order_by('id'))

    analytics_set = MenuItemPerformanceAnalytics.objects.all()
    current_datestamp=timezone.now()
    objs_to_create = []

    print(f'{MenuItemPerformanceTrends.__name__}:')
    for item in items:
        item_analytics = analytics_set.filter(menuItem_id=item)

        item_data = trends.calculate(item_analytics, TREND_TYPES)

        item_data['item'] = item

        obj = MenuItemPerformanceTrends(**item_data, current_datestamp=current_datestamp)
        print(f'{obj} | Size in Bytes: {sys.getsizeof(serialize("json", [obj]))}') #NOTE
        objs_to_create.append(obj)
    
    # TrendsModel.objects.bulk_create(objs_to_create)
    # print(f"\tNumber Created: {len(objs_to_create)}\n")

