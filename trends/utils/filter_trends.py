from django.utils import timezone
from django.core.serializers import serialize
import sys

from restaurants.models import (RestrictionTag, AllergyTag, IngredientTag, TasteTag, CookStyleTag)
from analytics.models import (RestrictionTagAnalytics, AllergiesTagAnalytics,
                              IngredientTagAnalytics, TasteTagAnalytics, 
                              CookStyleAnalytics, CalorieAnalytics)
from ..models import (RestrictionTagTrends, AllergyTagTrends,
                      IngredientTagTrends, TasteTagTrends, 
                      CookStyleTagTrends, CalorieTrends)
from . import trends


# (AnalyticsModel, TrendsModel, analytic_search_attr, analytic_history_attr)
FILTER_MODELS = [(RestrictionTag, RestrictionTagAnalytics, RestrictionTagTrends,
                        'number_of_search', 'number_of_HIS'),
                 (AllergyTag, AllergiesTagAnalytics, AllergyTagTrends,
                        'number_of_search', 'number_of_HIS'),
                 (IngredientTag, IngredientTagAnalytics, IngredientTagTrends, 
                        'number_of_search', 'number_of_HIS'),
                 (TasteTag, TasteTagAnalytics, TasteTagTrends, 
                        'number_of_search', 'number_of_HIS'),
                 (CookStyleTag, CookStyleAnalytics, CookStyleTagTrends, 
                        'number_of_search', 'number_of_HIS'),
                 (None, CalorieAnalytics, CalorieTrends, 
                        'number_of_searches', 'number_of_items_added_HIS')]


def driver():

    for TagModel, AnalyticsModel, TrendsModel, search_attr, history_attr in FILTER_MODELS:
        
        # (Trend Type, Analytic Attr)
        trend_types = [('search', search_attr), ('history', history_attr)]

        if TagModel is not None:
            tags = list(TagModel.objects.all().order_by('id'))
            analytic_tag_attr = 'tag_id'
            trend_tag_attr = 'tag'
        elif AnalyticsModel == CalorieAnalytics:
            tags = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            analytic_tag_attr = 'calorie_level'
            trend_tag_attr = 'calorie_level'
        else:
            print("Invalid Model Data")
            exit()

        analytics_set = AnalyticsModel.objects.all()
        current_datestamp=timezone.now()
        objs_to_create = []

        print(f'{TrendsModel.__name__}:')
        for tag in tags:
            tag_analytics = analytics_set.filter(**{analytic_tag_attr: tag})

            tag_data = trends.calculate(tag_analytics, trend_types)

            for entry in tag_data:
                entry[trend_tag_attr] = tag
                obj = TrendsModel(**entry, date_stamp=current_datestamp)

                print(f'{obj} | Size in Bytes: {sys.getsizeof(serialize("json", [obj]))}') #NOTE
                objs_to_create.append(obj)
        
        TrendsModel.objects.bulk_create(objs_to_create)     # @425 bytes per model, ~157.9K bulk per
        print(f"\tNumber Created: {len(objs_to_create)}\n")

        
        



        

            






# def calculate_trends(AnalyticsModel, trend_types):
    
#     print(f'{AnalyticsModel.__name__}:')
#     num_analytics = AnalyticsModel.objects.all().count()
#     if num_analytics < 5:
#         print(f'\tOnly {num_analytics} were found in database, while 5 are required.')
#         return
    
#     analytics = AnalyticsModel.objects.all().order_by('date_stamp')
#     first_timestamp = analytics[0].date_stamp.timestamp()
#     dates = [analytic.date_stamp.timestamp() - first_timestamp for analytic in analytics]

#     trend_data = []
#     for trend_type, analytic_attr in trend_types:
#         values = list(analytics.values_list(analytic_attr, flat=True))
#         coefficients = list(polyfit(dates, values, DEGREE)).reverse()

#         data = {'trend_type': trend_type}
#         for idx, coeff in enumerate(coefficients):
#             data[f'coeff{idx}'] = coeff
#         data['behavior'] = '' #TODO

#         trend_data.append(data)

#     return trend_data



