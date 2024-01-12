from django.utils import timezone

from analytics.models import AppSatisfactionAnalytics
from ..models import AppSatisfactionTrends
from . import trends


# (Trend Type, Analytic Attr)
TREND_TYPES = [('num_ratings', 'number_of_rating_total'), 
               ('avg_rating', 'average_rating')]


def driver(sim_datetime):

    analytics_set = AppSatisfactionAnalytics.objects.all()

    print(f'{AppSatisfactionTrends.__name__}:')
    trend_data = trends.calculate(analytics_set=analytics_set, 
                                  trend_types=TREND_TYPES,
                                  obj_string='App Satisfaction')
    if trend_data is not None:
        store_data(trend_data, sim_datetime)


def store_data(trend_data, sim_datetime):
    if sim_datetime is None:
        current_datestamp = timezone.now()
    else:
        current_datestamp = sim_datetime
    
    for entry in trend_data:
        # print(f'\t{entry}') #DEBUG
        obj = AppSatisfactionTrends.objects.create(**entry, date_stamp=current_datestamp)
        print(f'\t{obj}')
    print('\n')

