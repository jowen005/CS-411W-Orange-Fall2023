from django.utils import timezone

from analytics.models import AppSatisfactionAnalytics
from ..models import AppSatisfactionTrends
from . import trends


# (Trend Type, Analytic Attr)
TREND_TYPES = [('num_ratings', 'number_of_rating_total'), 
               ('avg_rating', 'average_rating')]


def driver():

    analytics_set = AppSatisfactionAnalytics.objects.all()

    print(f'{AppSatisfactionTrends.__name__}:')
    trend_data = trends.calculate(analytics_set=analytics_set, 
                                  trend_types=TREND_TYPES,
                                  obj_string='App Satisfaction')
    if trend_data is not None:
        store_data(trend_data)


def store_data(trend_data):
    current_datestamp = timezone.now()
    for entry in trend_data:
        # print(f'\t{entry}')
        obj = AppSatisfactionTrends.objects.create(**entry, date_stamp=current_datestamp)
        print(f'\t{obj}')
    print('\n')




# def calculate_trends():
#     print(f'{AppSatisfactionTrends.__name__}:')
#     num_analytics = AppSatisfactionAnalytics.objects.all().count()
#     if num_analytics < 5:
#         print(f'\tOnly {num_analytics} were found in database, while 5 are required.')
#         return
    
#     analytics = AppSatisfactionAnalytics.objects.all().order_by('date_stamp')
#     first_timestamp = analytics[0].date_stamp.timestamp()
#     dates = [analytic.date_stamp.timestamp() - first_timestamp for analytic in analytics]



#     trend_data = []
#     for trend_type, analytic_attr in TREND_TYPES:
#         values = list(analytics.values_list(analytic_attr, flat=True))
#         coefficients = list(polyfit(dates, values, DEGREE)).reverse()

#         data = {'trend_type': trend_type}
#         for idx, coeff in enumerate(coefficients):
#             data[f'coeff{idx}'] = coeff
#         data['behavior'] = '' #TODO

#         trend_data.append(data)

#     return trend_data


# def store_data(trend_data):
#     current_datestamp = timezone.now()

#     for entry in trend_data:
#         print(f'\t{entry}')
#         # obj = AppSatisfactionTrends.objects.create(**entry, date_stamp=current_datestamp)
#         # print(f'\t{obj}')
#     print('\n')
